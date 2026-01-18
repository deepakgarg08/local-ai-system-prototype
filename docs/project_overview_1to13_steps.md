**Berlin, Germany — 17 January 2026, 12:36 CET**

Below is a **complete, end-to-end project summary from STEP 1 through STEP 13**, written as a **canonical narrative**.
This is suitable for `docs/project_overview.md` or as a long-form architectural reference for future you / future LLM sessions.

---

# Project Summary — STEP 1 → STEP 13 (v0.1)

## Project Goal (From Day One)

Build a **local-first, cleanly architected Retrieval-Augmented Generation (RAG) system** from scratch with:

* explicit separation of concerns
* no hidden cloud dependency
* real local inference
* debuggable, inspectable behavior
* incremental correctness, not shortcuts

The system is designed to **answer questions grounded in user-provided documents**, not to act as a generic chatbot.

---

## Core Mental Model (Established Early)

The project is structured around a **strict two-phase model**:

### Offline (Build-Time)

```
documents → chunks → embeddings → vector index
```

### Online (Query-Time)

```
query → retrieve context → assemble prompt → LLM → answer
```

This separation is **never violated**.

---

## STEP-BY-STEP EVOLUTION

---

## STEP 1–4 — Project Skeleton & Architecture

### What Was Done

* Created the canonical project layout:

  * `docs/`
  * `data/raw/`, `data/processed/`, `data/indexes/`
  * `pipelines/`
  * `llms/`
* Established **clean architecture rules**:

  * capabilities ≠ orchestration
  * build-time ≠ query-time
* Declared `docs/` as the **source of truth** for design

### Outcome

A stable foundation where future steps could be reasoned about without ambiguity.

---

## STEP 5–7 — Offline Indexing Pipeline (Build-Time)

### What Was Done

* Implemented document ingestion from `data/raw/`
* Normalized and chunked documents
* Embedded chunks using `sentence-transformers`
* Built a FAISS index
* Persisted artifacts to disk:

  * `data/indexes/faiss.index`
  * `data/processed/chunks.json`

### Key Rule Enforced

> **Indexes are immutable at query time**

No auto-rebuilds. Missing artifacts = hard error.

---

## STEP 8–9 — Retrieval Layer (Query-Time)

### What Was Done

* Implemented FAISS-based semantic retrieval
* Added `retrieve_context(query, k)` in:

  ```
  pipelines/query/retriever.py
  ```
* Retrieval:

  * loads index from disk
  * embeds the query
  * returns top-k chunks (forced ranking)

### Important Property

Retrieval **always returns something**, even if irrelevant
(no relevance gating yet).

---

## STEP 10 — Prompt Assembly

### What Was Done

* Centralized prompt logic in:

  ```
  pipelines/prompting/assemble_prompt.py
  ```
* Prompt includes:

  * system instruction
  * retrieved context
  * strict rules (“answer only from context”)
* Supports optional `system_instruction`

### Architectural Rule

> Prompt logic lives in **one place only**

No duplication in pipelines.

---

## STEP 11 — LLM Capability Layer (Local)

### What Was Done

* Defined `BaseLLM` interface:

  ```python
  generate(prompt: str) -> str
  ```
* Implemented real local inference via Ollama:

  ```
  llms/ollama.py
  ```
* No mocks, no fake responses

### Outcome

The system could **actually generate answers**, locally.

---

## STEP 12 — LLM Infrastructure (12.1 → 12.4)

### STEP 12.1 — Local LLM Integration

* Verified real local inference
* No placeholders

### STEP 12.2 — Unified LLM Interface

* Introduced:

  ```
  llms/registry.py
  ```
* Pipelines stopped importing concrete LLMs
* Model choice centralized

### STEP 12.3 — Online LLM Capability

* Added:

  ```
  llms/openai.py
  ```
* OpenAI-style API support
* Introduced `.env` for secrets (shell-level only)

### STEP 12.4 — Config + Model Router

* Added:

  ```
  configs/runtime.py
  ```
* Environment-driven selection:

  * provider (`ollama` / `openai`)
  * model name
* Registry upgraded into a router
* Pipelines remained untouched

### Outcome

LLM infrastructure became:

* pluggable
* explicit
* policy-driven
* future-proof

---

## STEP 13 — End-to-End RAG Runner

### What Was Done

Created the **first real query-time execution pipeline**:

```
pipelines/query/run_rag.py
```

`run_rag()`:

1. Validates the query
2. Calls `retrieve_context()`
3. Normalizes retrieved chunks
4. Calls `assemble_prompt()`
5. Gets active LLM via `get_llm()`
6. Generates and returns an answer

### Critical Properties

* No invented abstractions
* No duplicated logic
* No UI / API server
* Pure orchestration

### What Was Discovered (Important)

* Vector search returns **forced matches**
* LLM answers even when context is irrelevant
* RAG ≠ grounding by default

This led to the **explicit recognition** that:

> **Relevance gating is required for trustworthiness**

---

## SYSTEM STATE AT END OF STEP 13 (v0.1)

### ✅ What Works

* Offline indexing
* FAISS retrieval
* Prompt assembly
* Local + online LLMs
* Unified routing
* End-to-end RAG execution

### ❌ What Is Not Yet Enforced

* Relevance validation
* Similarity thresholds
* Hallucination blocking
* Deterministic “I don’t know”

These are **known, accepted limitations** at v0.1.

---

## v0.1 FREEZE — WHAT IT MEANS

v0.1 represents:

* a **complete, runnable system**
* correct architecture
* correct abstractions
* incomplete correctness enforcement

This is the **right freeze point**.

---

## NEXT STEP (POST-v0.1)

### STEP 14 — Grounding & Retrieval Gating (v0.2)

Focus:

* expose FAISS distances
* define similarity thresholds
* block LLM calls on weak retrieval
* enforce grounded answers

This is where the system becomes **trustworthy**, not just functional.

---

## One-Line Summary

> **STEP 1–13 built the system correctly.
> STEP 14 will make it honest.**

If you want, next I can:

* format this as `docs/project_overview.md`
* derive a one-page architecture diagram (textual)
* or start STEP 14 cleanly on top of v0.1 
