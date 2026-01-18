# Instruction.md — Canonical Project Instruction File

This document is the **single authoritative instruction reference** for the Local‑First RAG System project.
It consolidates **all architectural decisions, constraints, goals, and assumptions** derived from:

* STEP 1–13 project evolution
* v0.1 freeze declaration
* query lifecycle description
* folder & architecture overviews
* detailed project description
* official Leistungsbeschreibung ("Lokales KI‑System")

---

## 1. Fundamental Philosophy

### 1.1 Human-in-the-Loop (Non‑Negotiable)

* The **human is always the final authority**.
* The system acts as a **junior assistant**, never an autonomous decision maker.
* All outputs **must be reviewable, editable, rejectable** by humans.
* No guarantees of correctness are implied or allowed.

> The system supports thinking. It does not replace responsibility.

---

## 2. Scope of the System

### 2.1 What the System IS

* A **local-first Retrieval‑Augmented Generation (RAG) system**
* Designed for **enterprise internal knowledge**
* Built with **clean architecture and explicit separation of concerns**
* Fully runnable **offline** (cloud optional, never mandatory)

### 2.2 What the System IS NOT

* Not a generic chatbot
* Not an autonomous agent
* Not a decision engine
* Not a black box
* Not a cloud‑dependent SaaS

---

## 3. Data Types (Authoritative)

Supported input data (pilot scope):

* PDFs (.pdf)
* Word (.docx)
* PowerPoint (.pptx)
* Text files (.txt)
* Emails (.eml / .msg)
* Images (.png / .jpg / .tiff) — OCR only

Explicitly excluded in v0.x:

* Excel
* Audio
* Video
* Image generation

---

## 4. User Expectations (Derived from Project PDF)

Users expect:

* Traceable answers
* Source references (document, section, page)
* Drafts, summaries, structured outputs
* Time savings in research

Users do NOT expect:

* Final decisions
* Legal guarantees
* Replacement of employees
* Fully correct answers

---

## 5. Core Architectural Law

### 5.1 Two‑Phase Model (Never Violated)

**Build‑Time (Offline)**

```
documents → chunks → embeddings → FAISS index
```

**Query‑Time (Online)**

```
query → retrieve context → assemble prompt → LLM → answer
```

Indexes are **immutable at query time**.

---

## 6. RAG System Responsibilities

The system:

* Ingests documents
* Parses and chunks them
* Builds semantic indexes
* Retrieves relevant context
* Generates answers **only from retrieved context**

The system does **not**:

* Decide relevance correctness (v0.1)
* Guarantee grounding (v0.1)
* Hide uncertainty

---

## 7. Roles & Permissions (Conceptual)

* Multiple user roles (e.g. Management, Accounting, Employees)
* Higher roles ⊇ lower roles
* Implemented via **separate vector indexes per role**

---

## 8. Performance & Queueing

* Local hardware is finite
* Simple queries execute immediately
* Complex queries may be queued
* Queueing prevents system blocking

---

## 9. Internet Usage (Isolated)

* Optional internet research
* Must be sandboxed
* **No access to internal documents**
* Prevents data leakage

---

## 10. Version Policy

* v0.1 = runnable, not trustworthy
* No refactoring during grounding work
* Each version freeze is explicit

---

## 11. Safety & Liability

* No business, legal, or technical liability
* Outputs are probabilistic suggestions
* Manual review is mandatory

---

## 12. Guiding Principle

> Build it correct first.
> Make it trustworthy second.
> Make it fast last.

#### .............................. TECHNICAL DETAILS...............

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

## Next Planned Step

### STEP 14 — Grounding & Retrieval Gating (v0.2)

Goals:

* Expose similarity scores
* Define relevance thresholds
* Block weak retrievals
* Enforce “I don’t know”

---

## Instruction to Future LLM

* Do NOT refactor v0.1 code
* Build grounding **on top**
* Preserve architecture
* Keep build‑time and query‑time separation

---

## End of Handoff

If you understand this context, continue with STEP 14.
