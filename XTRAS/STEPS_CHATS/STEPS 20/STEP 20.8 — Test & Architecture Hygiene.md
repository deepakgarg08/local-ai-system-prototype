**Berlin, Germany — 20 January 2026, 19:58 CET**

---

# STEP 20.8 — Test & Architecture Hygiene

This step is **not about new features**.
It is about **making the system safer to evolve** by enforcing discipline around **tests, structure, and boundaries**.

At this point in your project, the system already *works*.
Now we make sure it **keeps working when you change things**.

---

## 1️⃣ Why STEP 20.8 Exists (Conceptually)

As your RAG system grows, three risks appear:

1. **Silent regressions**
   Small refactors accidentally break retrieval, prompting, or ranking.

2. **Architecture erosion**
   Logic slowly leaks across layers (retriever doing prompt logic, tests depending on internals, etc.).

3. **Unclear intent**
   Future-you (or teammates) won’t know *why* a file or test exists.

STEP 20.8 fixes this by:

* Making architecture rules **explicit**
* Locking behavior with **tests**
* Creating **documentation at the same time as code**

This is what separates *a prototype* from *an engineering system*.

---

## 2️⃣ New Folder Structure Introduced

### 📁 Create a dedicated hygiene test area

```bash
mkdir -p tests/architecture_hygiene
```

**Why this folder exists**

* Keeps *non-functional* tests separate
* These tests don’t check “correct answers”
* They check **structure, contracts, and boundaries**

This prevents:

* Tests turning into a dumping ground
* Confusion between behavior tests and architecture tests

---

## 3️⃣ File 1: Architecture Boundary Test

### 📄 Create test file

```bash
touch tests/architecture_hygiene/test_layer_boundaries.py
```

### ✍️ Why this file exists

This test ensures:

* Retrieval layer does **not** import prompting
* Prompting layer does **not** import LLM implementations
* Query runner is the *only* orchestrator

This enforces your **clean architecture diagram in code**.

---

### 🧪 `test_layer_boundaries.py`

```python
import inspect
import pipelines.query.retriever as retriever
import pipelines.prompting.assemble_prompt as prompting


def test_retriever_does_not_import_prompting():
    source = inspect.getsource(retriever)
    assert "assemble_prompt" not in source


def test_prompting_does_not_import_llms():
    source = inspect.getsource(prompting)
    forbidden = ["ollama", "openai", "BaseLLM"]
    for name in forbidden:
        assert name not in source
```

### ✅ What this protects

* Prevents accidental circular dependencies
* Forces single responsibility per layer
* Makes refactors safer

If someone violates architecture → **tests fail immediately**

---

## 4️⃣ File 2: Public API Contract Test

### 📄 Create test file

```bash
touch tests/architecture_hygiene/test_public_contracts.py
```

### ✍️ Why this file exists

Your system has **public contracts**, even without an API server.

Examples:

* `retrieve_context(query, k)`
* `run_rag(query, top_k)`

These must remain stable.

---

### 🧪 `test_public_contracts.py`

```python
from pipelines.query.retriever import retrieve_context
from pipelines.query.run_rag import run_rag


def test_retrieve_context_contract():
    result = retrieve_context("test query", k=2)
    assert isinstance(result, list)


def test_run_rag_returns_string():
    answer = run_rag("What is this system?")
    assert isinstance(answer, str)
```

### ✅ What this protects

* You can refactor internals freely
* External behavior stays stable
* No accidental return-type changes

This is **API safety without an API**.

---

## 5️⃣ File 3: Hygiene Documentation (Very Important)

### 📄 Create documentation file

```bash
touch docs/architecture_hygiene.md
```

### ✍️ Why this file exists

Tests alone don’t explain *intent*.

This file answers:

* Why these tests exist
* What rules must never be broken
* How to extend the system safely

---

### 📝 `docs/architecture_hygiene.md`

```markdown
# Architecture Hygiene

This document defines non-negotiable structural rules of the system.

## Layer Boundaries

- Retrieval must not know about prompting
- Prompting must not know about LLM implementations
- LLMs must not know about retrieval or prompting
- Orchestration happens only in run_rag

## Why This Matters

Violating these rules:
- Causes hidden coupling
- Makes testing unreliable
- Breaks grounding guarantees later (v0.2+)

## Tests Enforcing This

See:
- tests/architecture_hygiene/test_layer_boundaries.py
- tests/architecture_hygiene/test_public_contracts.py
```

This document is **part of the architecture**, not “extra”.

---

## 6️⃣ Why This Step Is Good / Necessary

### Without STEP 20.8

* Every refactor is risky
* Architecture slowly degrades
* Bugs appear far from their cause

### With STEP 20.8

* Structure is enforced automatically
* Mistakes fail fast
* The system becomes **safe to grow**

This step:

* Enables STEP 21+
* Makes onboarding trivial
* Turns design decisions into executable rules

---

## 7️⃣ Mental Model to Keep

> **Features make the system useful**
> **Hygiene makes the system survivable**

STEP 20.8 is what allows your RAG system to evolve into a **long-lived, trustworthy codebase**.

If you want, next we can:

* Tie hygiene rules to **grounding guarantees**
* Add **anti-hallucination contract tests**
* Or formalize **v0.2 acceptance criteria**
