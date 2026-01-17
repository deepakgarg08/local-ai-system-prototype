What This Project Is

This project is a local-first Retrieval-Augmented Generation (RAG) system, built incrementally from scratch with a strong emphasis on:

clean architecture

explicit separation of concerns

local execution (no mandatory cloud dependency)

debuggability and observability

The system is designed to:

Ingest documents

Build semantic indexes offline

Retrieve relevant context at query time

Generate answers using pluggable LLM backends

Current State (As of Now)

The system currently has three fully real components:

1. Indexing (Build-Time)

Documents live in data/raw/

Offline pipelines clean, chunk, embed, and index them

Artifacts are written to data/indexes/ (e.g. FAISS index, chunks.json)

2. Retrieval (Query-Time)

Queries use vector similarity to retrieve relevant chunks

Retrieval reads from build-time artifacts only

No index rebuilding occurs during queries

3. Local LLM Integration

A real local LLM backend is implemented using Ollama

The LLM interface is defined in llms/base.py

A concrete implementation (OllamaLLM) lives in llms/ollama.py

No placeholders or mock responses are used

Architectural Principles

Capabilities vs orchestration

llms/ defines LLM capabilities

pipelines/ orchestrates workflows

Minimal contracts first

LLMs expose a minimal generate(prompt: str) -> str interface

Complexity (routing, agents, tools) is added only when required

Fail loudly, not silently

Query pipelines expect indexes to exist

Missing build artifacts are treated as errors, not auto-fixed

What Is Intentionally NOT Implemented Yet

The following are explicitly deferred and not part of the current system:

online / hosted LLM APIs

LLM routing or fallback logic

agents or tool-using loops

UI or API server

configuration-driven model switching

These will be introduced step-by-step once the core system is stable.

Mental Model to Use

Think of the system as:

Offline phase:
  documents → chunks → embeddings → index


Online phase:
  query → retrieve context → assemble prompt → LLM → answer

Everything in the codebase aligns to this model.

How to Continue From Here

Future steps will:

add a unified LLM router (local + online)

make model selection config-driven

connect retrieval + LLM into an end-to-end RAG runner

Until then, the focus is correctness, clarity, and clean boundaries.

This primer is intentionally short, explicit, and architecture-focused so that any new LLM session can immediately reason about the project without guessing.

# Project Directory Layout

This document defines the **canonical directory structure** of the project and explains the **responsibility of each folder**. It is intended to provide immediate context to new contributors or new LLM prompt sessions.

---

## Root Structure — `local-ai-system-prototype/`

```
local-ai-system-prototype/
│
├── docs/                     → architecture notes, design decisions, step-by-step docs
│                              (source of truth for system design)
│
├── data/
│   ├── raw/                  → original input documents (PDF, DOCX, TXT)
│                              (never modified after ingestion)
│   ├── processed/            → cleaned, normalized, and chunked text
│                              (output of ingestion + chunking pipelines)
│   └── indexes/              → build-time artifacts for retrieval
│                              (FAISS index files, chunks.json, metadata snapshots)
│
├── llms/                     → LLM capability layer (CORE INFRASTRUCTURE)
│   ├── base.py               → abstract BaseLLM contract (single source of truth)
│   └── ollama.py             → local LLM implementation using Ollama
│                              (real inference, no placeholders)
│
├── pipelines/                → execution pipelines (build-time + query-time)
│   ├── indexing/             → offline pipelines to build embeddings and indexes
│   ├── query/                → runtime query pipelines (retrieval, prompt assembly)
│   │   └── retriever.py      → retrieves relevant chunks from vector index
│   └── llm/                  → temporary execution/tests related to LLM usage
│                              (consumes llms/, does not define LLMs)
│
├── models/                   → local model files (future)
│                              (downloaded LLMs, embedding models, weights)
│
├── vectorstores/             → semantic storage backends (future)
│                              (FAISS, hybrid search, BM25 + vectors)
│
├── app/                      → application layer (future)
│                              (API server, UI, request handling)
│
├── configs/                  → configuration & environment settings (future)
│                              (model selection, paths, runtime toggles)
│
├── scripts/                  → admin and utility scripts (future)
│                              (rebuild index, health checks, maintenance tasks)
│
├── tests/                    → test scaffolding
│                              (unit, integration, retrieval-quality tests)
│
├── logs/                     → runtime and audit logs
│                              (query traces, errors, performance metrics)
│
├── pyproject.toml            → project metadata, dependencies, packaging config
├── README.md                 → project overview and usage instructions
└── .venv/                    → Python virtual environment (local, not committed)
```

---

## Architectural Rules Implied by This Layout

* **Capabilities vs execution are separated**

  * `llms/` defines *what an LLM is and how to call it*
  * `pipelines/` orchestrates *when and why it is called*

* **Build-time vs query-time are separated**

  * Indexes are created offline (`pipelines/indexing/`)
  * Queries never rebuild indexes (`pipelines/query/`)

* **Future folders are intentional placeholders**

  * Their presence communicates roadmap and boundaries
  * They are not required to exist until implemented

---

This layout should be treated as **canonical** for the project.
