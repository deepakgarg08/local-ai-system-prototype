**Berlin, Germany — 17 January 2026, 11:40 CET**

Yes — **renaming this to STEP 13 makes perfect sense**, and it’s the *correct architectural move*.

Let me explain **why**, then we’ll define **STEP 13** cleanly and precisely.

---

## Why STEP 12 Should End at 12.4

STEP 12 was about **LLM infrastructure**, not RAG execution.

What STEP 12 now fully covers:

| Substep | Purpose               | Status |
| ------- | --------------------- | ------ |
| 12.1    | Real local LLM        | ✅      |
| 12.2    | Unified LLM interface | ✅      |
| 12.3    | Online LLM capability | ✅      |
| 12.4    | Config + model router | ✅      |

All of these are about **how an LLM is selected and invoked**.

They do **not** yet answer:

> “How does a user query flow through retrieval → prompt → LLM → answer?”

That is a **new concern**.

So yes — **End-to-End RAG Runner deserves its own step**.

---

## Canonical Rename (Recommended)

### ✅ STEP 13 — End-to-End RAG Runner (Query → Answer)

This keeps the project logically layered:

* **STEP 12** → LLM infrastructure (capabilities + policy)
* **STEP 13** → RAG execution pipeline

This is exactly how mature systems are structured.

---

## What STEP 13 Will Do (Scope Lock)

STEP 13 will introduce:

* one callable RAG pipeline
* explicit wiring of:

  * retriever
  * prompt assembly
  * unified LLM
* a **single entry function** like:

```python
answer = run_rag(query: str)
```

And **nothing else**.

No UI
No API server
No agents
No tools

---

## Where STEP 13 Will Live

Proposed location (clean and canonical):

```
pipelines/query/run_rag.py
```

This matches your existing layout:

* `pipelines/indexing/` → build-time
* `pipelines/query/` → runtime
* `run_rag.py` → orchestration, not capability

---

## High-Level Data Flow (STEP 13)

```
query (str)
  ↓
Retriever (FAISS)
  ↓
Top-k chunks
  ↓
Prompt assembly
  ↓
get_llm()
  ↓
generate()
  ↓
answer (str)
```

Every component already exists.
STEP 13 is **only wiring**.

---

## What We’ll Do Next (If You Confirm)

If you say yes, the next response will:

1. Define the **exact contract** of `run_rag`
2. Implement `pipelines/query/run_rag.py`
3. Keep all logic explicit and debuggable
4. Add a minimal manual test

No refactors. No surprises.

---

## Final Answer

✔ Yes, renaming is correct
✔ Yes, it improves conceptual clarity
✔ Yes, STEP 13 should start now

If you’re ready, reply with:

> **“Proceed with STEP 13 — End-to-End RAG Runner”**

And we’ll finish this milestone properly.


**Berlin, Germany — 17 January 2026, 12:24 CET**

Below is a **clean, architecture-level summary of STEP 13**, followed by the **clear next steps**.
This is written so it can be copied directly into `docs/` as a milestone record.

---

# STEP 13 — End-to-End RAG Runner

**Status: Implemented (without grounding guards yet)**

## Purpose of STEP 13

STEP 13 introduced the **first real end-to-end execution path** of the system:

```
query → retrieve context → assemble prompt → LLM → answer
```

The goal was **wiring**, not correctness enforcement.

---

## Files & Folders Involved

### ✅ New File Created

```
pipelines/query/run_rag.py
```

This file did **not exist before STEP 13**.

---

### 🔁 Existing Files Reused (No Logic Duplicated)

```
pipelines/query/retriever.py
```

* Provides `retrieve_context(query, k)`
* FAISS-based semantic retrieval
* Returns top-k text chunks (forced ranking)

```
pipelines/prompting/assemble_prompt.py
```

* Centralized prompt construction
* Enforces “answer only from context” instruction
* Supports optional `system_instruction`

```
llms/registry.py
```

* Unified LLM access point
* Routes to local or online LLM based on config

No changes were made to these files in STEP 13.

---

## What `run_rag.py` Does

`run_rag()` is **pure orchestration**.

It:

1. Validates the user query
2. Calls `retrieve_context()` to get top-k chunks
3. Normalizes chunks for prompt assembly
4. Calls `assemble_prompt()` (with `system_instruction=None`)
5. Gets the active LLM via `get_llm()`
6. Calls `llm.generate(prompt)`
7. Returns the answer

**Important:**
It does **not** decide:

* which LLM is used
* whether context is good enough
* how relevance is measured

That is intentional.

---

## Architectural Guarantees Achieved

After STEP 13, the system guarantees:

* ✅ Full query-time execution path exists
* ✅ Retrieval, prompting, and LLM concerns remain separated
* ✅ No duplicated prompt logic
* ✅ No fake abstractions (no invented `Retriever` class)
* ✅ Pipelines remain backend-agnostic
* ✅ Local-first, but online-capable

---

## What STEP 13 Explicitly Does *Not* Solve

This is critical:

STEP 13 **does not guarantee correctness or grounding**.

Specifically, it does **not** prevent:

* irrelevant chunks being retrieved
* low-similarity matches being used
* LLM answering from its internal knowledge
* hallucinations on out-of-domain queries

This was **observed and confirmed** during testing.

That behavior is expected at this stage.

---

## Current System State After STEP 13

```
Indexing (offline)        ✅
Retrieval (FAISS)         ✅ (forced ranking only)
Prompt assembly           ✅
Unified LLM routing       ✅
End-to-end RAG runner     ✅
Grounding enforcement     ❌
Relevance gating          ❌
Hallucination blocking    ❌
```

---

# What Comes Next (Correct Next Steps)

## 🔜 STEP 14 — Grounding & Retrieval Gating (Highest Priority)

This step will:

* expose FAISS similarity distances
* define a similarity threshold
* block LLM calls when context is insufficient
* force “I don’t know” responses
* optionally add debug logging for retrieval scores

This is the step that transforms your system from:

> *RAG-augmented chatbot*
> to
> *document-grounded assistant*

---

## Optional Later Steps (After STEP 14)

* STEP 15 — Evaluation harness (test questions + expected behavior)
* STEP 16 — Minimal CLI
* STEP 17 — Observability / tracing
* STEP 18 — Agents or tools (if ever needed)

---

## Final One-Line Summary

> **STEP 13 proved the system works end-to-end; STEP 14 will prove it is trustworthy.**

When you’re ready, say:

> **“Proceed with STEP 14 — Grounding & Retrieval Gating”**
