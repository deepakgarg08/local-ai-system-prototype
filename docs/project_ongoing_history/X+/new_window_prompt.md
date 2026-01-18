# new_window_prompt.md — Canonical Context Handoff

Paste this file **verbatim** into a new ChatGPT window to restore full project context.

---

## Project Name

**Local‑First RAG System (Clean Architecture Prototype)**

---

## One‑Line Summary

A clean, local‑first Retrieval‑Augmented Generation system built end‑to‑end (v0.1), intentionally frozen before grounding enforcement, designed for enterprise document understanding with strict human‑in‑the‑loop control.

---

## Mental Model (Canonical)

### Offline / Build‑Time

```
documents → chunks → embeddings → FAISS index
```

### Online / Query‑Time

```
query → retrieve context → assemble prompt → LLM → answer
```

This separation is **never violated**.

---

## Current Version

### v0.1 — Frozen

* End‑to‑end runnable
* Correct architecture
* No relevance gating
* No hallucination blocking
* No enforced “I don’t know”

This is intentional.

---

## What Works

* Offline indexing (FAISS)
* Disk‑backed artifacts
* Query‑time retrieval
* Centralized prompt assembly
* Local LLM (Ollama)
* Online LLM (OpenAI‑style API)
* Unified BaseLLM interface
* Config‑driven routing
* End‑to‑end `run_rag()` pipeline

---

## What Is NOT Solved Yet

* Similarity thresholds
* Relevance validation
* Grounding enforcement
* Hallucination blocking
* Deterministic refusal

---

## Canonical Directory Structure (v0.1)

```
local-ai-system-prototype/
│
├── docs/
│   └── v0.1.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── indexes/
│       └── faiss.index
│
├── llms/
│   ├── base.py
│   ├── ollama.py
│   ├── openai.py
│   └── registry.py
│
├── configs/
│   └── runtime.py
│
├── pipelines/
│   ├── indexing/
│   ├── prompting/
│   │   └── assemble_prompt.py
│   └── query/
│       ├── retriever.py
│       └── run_rag.py
│
├── .env
├── pyproject.toml
└── README.md
```

---

## System Philosophy

* Local‑first
* Fail‑loud
* Explicit abstractions
* No hidden magic
* Human always decides

---

## User Data Characteristics

* Enterprise internal documents
* Specifications (700–1000 pages)
* Contracts & policies
* Training material

Expectations:

* Traceable answers
* Source references
* Reviewable drafts

---


Current version = v0.2

STEP 14 is complete

Next work is refinement

If this is not updated, a new window will incorrectly assume:

“grounding is planned but not implemented”

—which would be wrong and dangerous.

New Canonical Status (You Can Treat This as Official)

v0.2 = grounded, gated, test-proven RAG system
The system now enforces honesty over helpfulness.

This aligns perfectly with:

the Leistungsbeschreibung

human-in-the-loop philosophy

enterprise safety expectations
