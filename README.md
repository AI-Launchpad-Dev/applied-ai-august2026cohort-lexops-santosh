# LexOps — Contract Intelligence & Compliance Copilot
## Milestone-Wise Code Submission

Prepared by: Santosh Kumar Chintala
Applied AI Professional Certification Program, IIT Hyderabad

---

## How to run this code

1. Copy these files into the project root (alongside the `datagen/` package and `data/lexops/` generated data — see the Data Generation Toolkit section of the main report for setup).
2. Activate the virtual environment and ensure `.env` has a valid `DATAGEN_GEMINI_API_KEY` and, for M7, `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` / `LANGFUSE_BASE_URL`.
3. Run each milestone file directly with `python mX_<name>.py` (see per-file notes below). Files are numbered in the order they should be run/reviewed.

---

## File-by-file guide

| File | Milestone | What it does | How to run |
|---|---|---|---|
| `m1_extract.py` | M1 | Extracts a validated `ContractSummary` from raw intake requests; scores against built-in ground truth using fuzzy word-overlap matching. | `python m1_extract.py` |
| `m2_agent.py` | M2 | Single tool-using agent (clause-risk calculator, renewal calendar, memo writer) with a hand-built ReAct loop. | `python m2_agent.py` |
| `m3_memory.py` | M3 | Per-counterparty negotiation memory (SQLite) + semantic playbook index (Chroma + Gemini embeddings). | `python m3_memory.py` |
| `m4_rag.py` | M4 | Hybrid (BM25 + semantic) search, LLM reranking, cited answers, independent groundedness check; runs against real eval cases. | `python m4_rag.py` |
| `m5_workflow.py` | M5 | LangGraph state machine: extract → compare → draft → conditional route, with checkpointing. | `python m5_workflow.py` |
| `m6_mcp_server.py` | M6 | MCP server exposing the contract repository / e-signature mock API. | Launched automatically by `m6_multi_agent.py` — no need to run directly. |
| `m6_multi_agent.py` | M6 | Four-agent team (Extraction, Playbook RAG, Redline Drafter, Legal Reviewer) calling the MCP server for reads and writes. | `python m6_multi_agent.py` |
| `m7_observability.py` | M7 | LangFuse-traced pipeline + long-document (map-reduce) hardening + per-agent failure fallback. | `python m7_observability.py` |
| `m8_eval_runner.py` | M8 | Guarded-answer pipeline scored against the 23-case golden eval set; writes `eval_results.json`. | `python m8_eval_runner.py` |
| `m8_api.py` | M8 | FastAPI deployment wrapping the full pipeline as a `/review` endpoint. | `pip install fastapi uvicorn` then `uvicorn m8_api:app --reload` |

---

## Dependencies by milestone

```
# Core (all milestones)
pydantic, requests  (already required by the data-generation toolkit)

# M3
pip install chromadb

# M4
pip install rank_bm25

# M5
pip install langgraph

# M6
pip install mcp

# M7
pip install langfuse python-dotenv

# M8
pip install fastapi uvicorn
```

---

## Notes for reviewers

- **M1–M2** are self-contained and require only a Gemini API key.
- **M3** requires the corpus to already be generated (`data/lexops/corpus/markdown/*.md`) and will build a persistent Chroma index on first run — subsequent runs skip re-embedding.
- **M4** depends on M3's Chroma index already existing.
- **M5** imports directly from `m1_extract.py` and `m2_agent.py` and `m4_rag.py` — keep all files in the same directory.
- **M6** spins up `m6_mcp_server.py` as an in-process MCP server object (not a subprocess) — no separate terminal needed.
- **M7** requires a free LangFuse account (cloud.langfuse.com) and will print a warning (not an error) if credentials are missing — the pipeline still runs, just without traces.
- **M8**'s `m8_eval_runner.py` is the final, corrected version after three rounds of guardrail-scoring fixes (documented in the main report) — every failure across those rounds was traced to the scoring harness using naive substring matching, not the underlying model. The negation-aware checks in this file are the fix.

---

## Final evaluation result

22 / 23 golden-set cases passed (95.7%). The one documented near-miss (case `LEXOPS-EV-902`) is an intentionally strict guardrail case and is explained in the main report rather than patched further.
