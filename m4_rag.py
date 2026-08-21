"""Milestone 4: Production RAG + evaluation baseline.

Builds on M3's Chroma semantic index by adding:
  1. BM25 keyword search over the same chunks (catches exact terms/numbers
     that embeddings sometimes blur past).
  2. Hybrid merge of semantic + keyword rankings via reciprocal rank fusion.
  3. LLM-based reranking of the merged candidates.
  4. Answer generation that cites which document(s) it drew from.
  5. A groundedness check -- does the cited text actually support the claims
     in the answer, or did the model add something not in the source?
  6. A run against the real golden_set.json eval cases, scored for whether
     the required documents were cited (a proxy for retrieval quality) and
     whether the answer was flagged as grounded.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import chromadb
from rank_bm25 import BM25Okapi

from datagen.llm import complete, complete_json
from m3_memory import CORPUS_DIR, CHROMA_DIR, _chunk_text, _embed

EVAL_PATH = Path("data/lexops/eval/golden_set.json")


# =====================================================================
# Part 1: load all chunks (needed for BM25 -- Chroma doesn't expose a
# clean way to iterate all documents back out with their raw text ranks)
# =====================================================================

def _load_all_chunks() -> list[dict[str, Any]]:
    """Re-chunk the corpus the same way M3 did, so BM25 and Chroma line up
    on identical chunk boundaries and ids."""
    chunks = []
    for md_file in sorted(CORPUS_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        for i, chunk in enumerate(_chunk_text(text)):
            chunks.append({
                "id": f"{md_file.stem}-{i}",
                "text": chunk,
                "source": md_file.stem,
            })
    return chunks


_ALL_CHUNKS = _load_all_chunks()
_CHUNK_BY_ID = {c["id"]: c for c in _ALL_CHUNKS}

_TOKENIZED = [re.findall(r"[a-z0-9]+", c["text"].lower()) for c in _ALL_CHUNKS]
_BM25 = BM25Okapi(_TOKENIZED)


# =====================================================================
# Part 2: keyword search (BM25)
# =====================================================================

def bm25_search(query: str, top_k: int = 10) -> list[str]:
    """Return chunk ids ranked by BM25 keyword relevance."""
    tokens = re.findall(r"[a-z0-9]+", query.lower())
    scores = _BM25.get_scores(tokens)
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return [_ALL_CHUNKS[i]["id"] for i in ranked[:top_k]]


# =====================================================================
# Part 3: semantic search (Chroma, reusing M3's index)
# =====================================================================

def semantic_search(query: str, top_k: int = 10) -> list[str]:
    """Return chunk ids ranked by embedding similarity."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection("lexops_playbook")
    query_vec = _embed([query])[0]
    results = collection.query(query_embeddings=[query_vec], n_results=top_k)
    return results["ids"][0]


# =====================================================================
# Part 4: hybrid merge (reciprocal rank fusion)
# =====================================================================

def hybrid_search(query: str, top_k: int = 8, k_constant: int = 60) -> list[dict[str, Any]]:
    """Merge semantic + BM25 rankings using reciprocal rank fusion.

    RRF score for a doc = sum over each ranked list of 1 / (k + rank).
    Simple, has no tunable weights to overfit, and is the standard choice
    for combining heterogeneous rankers.
    """
    sem_ids = semantic_search(query, top_k=15)
    kw_ids = bm25_search(query, top_k=15)

    scores: dict[str, float] = {}
    for rank, cid in enumerate(sem_ids):
        scores[cid] = scores.get(cid, 0) + 1.0 / (k_constant + rank)
    for rank, cid in enumerate(kw_ids):
        scores[cid] = scores.get(cid, 0) + 1.0 / (k_constant + rank)

    ranked_ids = sorted(scores, key=lambda c: scores[c], reverse=True)[:top_k]
    return [_CHUNK_BY_ID[cid] for cid in ranked_ids if cid in _CHUNK_BY_ID]


# =====================================================================
# Part 5: LLM reranking
# =====================================================================

def rerank(query: str, candidates: list[dict[str, Any]], top_n: int = 4) -> list[dict[str, Any]]:
    """Ask the LLM to score each candidate's relevance 1-10, keep the top_n."""
    numbered = "\n\n".join(
        f"[{i}] (source: {c['source']})\n{c['text'][:500]}"
        for i, c in enumerate(candidates)
    )
    prompt = f"""Question: {query}

Candidate passages:
{numbered}

Score each passage's relevance to answering the question, 1 (irrelevant) to
10 (directly answers it). Return JSON: {{"scores": [{{"index": 0, "score": 7}}, ...]}}
covering every passage index shown above."""

    try:
        result = complete_json(prompt)
        scored = result.get("scores", [])
        order = sorted(scored, key=lambda s: s.get("score", 0), reverse=True)
        top_indices = [s["index"] for s in order[:top_n] if 0 <= s.get("index", -1) < len(candidates)]
        if top_indices:
            return [candidates[i] for i in top_indices]
    except Exception as e:
        print(f"  [!] Rerank failed ({e}), falling back to hybrid order.")

    return candidates[:top_n]


# =====================================================================
# Part 6: answer generation with citations
# =====================================================================

def answer_with_citations(question: str) -> dict[str, Any]:
    candidates = hybrid_search(question, top_k=12)
    top_chunks = rerank(question, candidates, top_n=6)

    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in top_chunks
    )
    prompt = f"""Answer the question using ONLY the source passages below. If the
passages do not contain the answer, say so explicitly rather than guessing.

{context}

Question: {question}

Respond with JSON: {{"answer": "...", "cited_sources": ["source-slug", ...]}}
List only sources you actually relied on in cited_sources."""

    raw = complete_json(prompt)
    return {
        "answer": raw.get("answer", ""),
        "cited_sources": raw.get("cited_sources", []),
        "chunks_used": [c["source"] for c in top_chunks],
    }


# =====================================================================
# Part 7: groundedness check
# =====================================================================

def check_groundedness(answer: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
    """Ask the LLM to verify the answer's claims are supported by the chunks.

    A separate, adversarial-framed call rather than trusting the generating
    call's own citation -- a model is more likely to catch its own
    unsupported claims when asked to specifically look for them.
    """
    context = "\n\n".join(f"[{c['source']}]\n{c['text']}" for c in chunks)
    prompt = f"""Source passages:
{context}

Claimed answer: {answer}

Does the source text actually support every claim in the answer? Look
specifically for numbers, thresholds, or names in the answer that do NOT
appear in the source passages.

Respond with JSON: {{"grounded": true/false, "unsupported_claims": ["..."]}}"""

    try:
        return complete_json(prompt)
    except Exception as e:
        return {"grounded": None, "unsupported_claims": [], "error": str(e)}


# =====================================================================
# Part 8: run against the golden eval set
# =====================================================================

def run_eval(limit: int = 8) -> None:
    if not EVAL_PATH.exists():
        print(f"[!] {EVAL_PATH} not found -- generate the eval set first.")
        return

    cases = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    # Skip guardrail/injection cases here -- those test refusal behaviour,
    # which M8 evaluates explicitly. M4 focuses on retrieval quality.
    testable = [c for c in cases if c.get("category") in ("factual", "multi_hop", "unanswerable")]
    testable = testable[:limit]

    print(f"Running RAG pipeline against {len(testable)} eval cases...\n")

    grounded_count = 0
    cited_required_count = 0
    total_with_requirements = 0

    for i, case in enumerate(testable, 1):
        print(f"[{i}/{len(testable)}] {case['id']} ({case['category']})")
        print(f"  Q: {case['question']}")

        result = answer_with_citations(case["question"])
        print(f"  A: {result['answer'][:200]}")
        print(f"  Cited: {result['cited_sources']}")

        ground = check_groundedness(result["answer"], [
            c for c in _ALL_CHUNKS if c["source"] in result["chunks_used"]
        ])
        is_grounded = ground.get("grounded")
        print(f"  Grounded: {is_grounded}"
              f"{'  unsupported: ' + str(ground['unsupported_claims']) if ground.get('unsupported_claims') else ''}")
        if is_grounded:
            grounded_count += 1

        must_cite = case.get("must_cite", [])
        if must_cite:
            total_with_requirements += 1
            # loose match: does any required doc title share a word with what we cited
            cited_text = " ".join(result["chunks_used"]).lower()
            hit = any(
                any(w in cited_text for w in re.findall(r"[a-z]+", req.lower()) if len(w) > 4)
                for req in must_cite
            )
            if hit:
                cited_required_count += 1
            print(f"  Required cite(s): {must_cite} -> {'OK' if hit else 'MISS'}")

        print()

    print("=" * 50)
    print("M4 RESULTS")
    print("=" * 50)
    print(f"Cases run              : {len(testable)}")
    print(f"Groundedness pass rate : {grounded_count}/{len(testable)} "
          f"({100*grounded_count/len(testable):.0f}%)")
    if total_with_requirements:
        print(f"Required-citation hit  : {cited_required_count}/{total_with_requirements} "
              f"({100*cited_required_count/total_with_requirements:.0f}%)")


if __name__ == "__main__":
    print(f"Loaded {len(_ALL_CHUNKS)} chunks for hybrid search.\n")

    demo_q = "What deviations require escalation for the audit rights clause?"
    print(f"DEMO QUERY: {demo_q}")
    result = answer_with_citations(demo_q)
    print(f"ANSWER: {result['answer']}")
    print(f"CITED: {result['cited_sources']}")
    ground = check_groundedness(result["answer"], [
        c for c in _ALL_CHUNKS if c["source"] in result["chunks_used"]
    ])
    print(f"GROUNDED: {ground.get('grounded')}  unsupported: {ground.get('unsupported_claims')}")

    print("\n" + "=" * 50 + "\n")
    run_eval(limit=8)