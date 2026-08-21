"""Milestone 3: Persistent memory + semantic index.

Two pieces:
  1. Per-counterparty negotiation memory -- a local SQLite table keyed by
     counterparty_id, seeded from mock_api data and appendable as new
     negotiation rounds happen.
  2. A Chroma vector index over the 19 playbook markdown documents, using
     Gemini's embedding API, so the agent can search by meaning rather than
     exact keyword.
"""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any

import chromadb
import requests

from datagen.config import settings

MOCK_API_DIR = Path("data/lexops/mock_api")
CORPUS_DIR = Path("data/lexops/corpus/markdown")
DB_PATH = Path("data/lexops/negotiation_memory.sqlite")
CHROMA_DIR = Path("data/lexops/chroma_store")

EMBED_MODEL = "models/gemini-embedding-001"


# =====================================================================
# Part 1: per-counterparty negotiation memory (SQLite)
# =====================================================================

def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS negotiation_rounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            counterparty_id TEXT NOT NULL,
            round_number INTEGER,
            note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn


def seed_memory_from_mock_data() -> int:
    """Populate initial negotiation history from mock_api/counterparties.csv.

    Uses the negotiation_rounds_to_date field already generated for each
    counterparty as a starting point -- real usage would append new rounds
    over time via record_negotiation_round().
    """
    path = MOCK_API_DIR / "counterparties.csv"
    if not path.exists():
        print(f"[!] {path} not found -- generate mock_api tables first.")
        return 0

    conn = _get_conn()
    # Avoid re-seeding on every run.
    existing = conn.execute("SELECT COUNT(*) FROM negotiation_rounds").fetchone()[0]
    if existing > 0:
        print(f"Memory already seeded ({existing} rows) -- skipping.")
        conn.close()
        return existing

    count = 0
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rounds = int(row.get("negotiation_rounds_to_date", 0) or 0)
            posture = row.get("historical_posture", "unknown")
            for r in range(1, rounds + 1):
                conn.execute(
                    "INSERT INTO negotiation_rounds (counterparty_id, round_number, note) "
                    "VALUES (?, ?, ?)",
                    (row["counterparty_id"], r,
                     f"Round {r}: counterparty posture observed as '{posture}'."),
                )
                count += 1
    conn.commit()
    conn.close()
    print(f"Seeded {count} negotiation-round rows.")
    return count


def record_negotiation_round(counterparty_id: str, note: str) -> None:
    """Append a new negotiation round -- call this as real rounds happen."""
    conn = _get_conn()
    last = conn.execute(
        "SELECT COALESCE(MAX(round_number), 0) FROM negotiation_rounds WHERE counterparty_id = ?",
        (counterparty_id,),
    ).fetchone()[0]
    conn.execute(
        "INSERT INTO negotiation_rounds (counterparty_id, round_number, note) VALUES (?, ?, ?)",
        (counterparty_id, last + 1, note),
    )
    conn.commit()
    conn.close()


def get_negotiation_history(counterparty_id: str) -> list[dict[str, Any]]:
    """Return all past negotiation rounds for a counterparty, oldest first."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT round_number, note, created_at FROM negotiation_rounds "
        "WHERE counterparty_id = ? ORDER BY round_number",
        (counterparty_id,),
    ).fetchall()
    conn.close()
    return [{"round": r[0], "note": r[1], "created_at": r[2]} for r in rows]


# =====================================================================
# Part 2: semantic index over the playbook (Chroma + Gemini embeddings)
# =====================================================================

import time


def _embed(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts using Gemini's embedding API.

    One request per text, with a small delay between calls and retry with
    backoff on 429s -- free-tier embedding quotas are stricter than the main
    chat model's, so firing 60+ requests back-to-back trips the limit fast.
    """
    vectors = []
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"{EMBED_MODEL}:embedContent"
    )
    for i, text in enumerate(texts, 1):
        for attempt in range(6):
            resp = requests.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": settings.gemini_api_key,
                },
                json={
                    "content": {"parts": [{"text": text}]},
                    "outputDimensionality": 768,
                },
                timeout=60,
            )
            if resp.status_code == 429:
                wait = 2 ** attempt
                print(f"  [{i}/{len(texts)}] rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            vectors.append(resp.json()["embedding"]["values"])
            break
        else:
            raise RuntimeError(f"Failed to embed chunk {i} after repeated 429s.")

        # Small pause between successful calls to stay under rate limits.
        time.sleep(1.0)
        if i % 10 == 0:
            print(f"  embedded {i}/{len(texts)}...")

    return vectors


def _chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """Naive word-count chunker -- good enough for a 19-document corpus."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap
    return chunks


def build_playbook_index() -> int:
    """Chunk + embed every playbook markdown file into a Chroma collection."""
    if not CORPUS_DIR.exists():
        print(f"[!] {CORPUS_DIR} not found -- generate the corpus first.")
        return 0

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection("lexops_playbook")

    if collection.count() > 0:
        print(f"Index already built ({collection.count()} chunks) -- skipping.")
        return collection.count()

    ids, docs, metadatas = [], [], []
    for md_file in sorted(CORPUS_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        for i, chunk in enumerate(_chunk_text(text)):
            ids.append(f"{md_file.stem}-{i}")
            docs.append(chunk)
            metadatas.append({"source": md_file.stem})

    print(f"Embedding {len(docs)} chunks from {len(list(CORPUS_DIR.glob('*.md')))} documents...")
    embeddings = _embed(docs)

    collection.add(ids=ids, documents=docs, metadatas=metadatas, embeddings=embeddings)
    print(f"Indexed {len(docs)} chunks.")
    return len(docs)


def search_playbook(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Semantic search over the playbook. Returns top_k chunks with source."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection("lexops_playbook")

    if collection.count() == 0:
        return [{"error": "Index is empty -- run build_playbook_index() first."}]

    query_vec = _embed([query])[0]
    results = collection.query(query_embeddings=[query_vec], n_results=top_k)

    hits = []
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        hits.append({"source": meta["source"], "text": doc[:300], "distance": dist})
    return hits


# =====================================================================
# Demo
# =====================================================================

if __name__ == "__main__":
    print("=== Seeding negotiation memory ===")
    seed_memory_from_mock_data()

    print("\n=== Building playbook semantic index (one-time, costs API calls) ===")
    build_playbook_index()

    print("\n=== Demo: negotiation history lookup ===")
    conn = _get_conn()
    sample_id = conn.execute(
        "SELECT DISTINCT counterparty_id FROM negotiation_rounds LIMIT 1"
    ).fetchone()
    conn.close()
    if sample_id:
        history = get_negotiation_history(sample_id[0])
        print(f"History for {sample_id[0]}:")
        for h in history:
            print(f"  round {h['round']}: {h['note']}")

    print("\n=== Demo: semantic playbook search ===")
    query = "What happens if the counterparty refuses to cap liability?"
    print(f"Query: {query}")
    for hit in search_playbook(query):
        print(f"  [{hit.get('source')}] (distance={hit.get('distance', 0):.3f}) {hit.get('text', hit.get('error'))}")