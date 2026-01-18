# STEP 17 — Retrieval Quality Optimization (Tests)

This folder contains **focused regression and behavior tests** introduced in  
**STEP 17: Retrieval Quality Optimization**.

The purpose of these tests is **not** to validate model outputs, but to lock in
**architectural safety guarantees** around retrieval quality and hallucination
containment.

---

## What STEP 17 Tests Protect

STEP 17 introduces retrieval-aware controls that decide:

- **when the system is allowed to answer**
- **how strictly the LLM is constrained**
- **when extractive-only mode must be enforced**

These tests ensure those decisions **cannot regress silently**.

---

## Test Files Overview

### `test_extractive_mode_activation.py`
Guards the rule:

> *Small corpus + limited evidence → extractive-only mode must activate*

This prevents small or weaker LLMs from hallucinating by forcing them to
quote or closely paraphrase retrieved context.

---

### `test_prompt_assembly_extractive.py`
Verifies prompt-level safety:

- extractive instructions are injected when enabled
- extractive instructions are absent when disabled

This ensures hallucination containment lives **in the prompt layer**, not
in model behavior.

---

### `test_safety_regression.py`
Regression test to ensure STEP 17 does **not weaken earlier guarantees**:

- If grounding fails, the LLM must **never be called**
- Refusal behavior remains deterministic

---

## What Is Intentionally NOT Tested

These tests do **not** cover:

- answer correctness
- wording quality
- FAISS retrieval accuracy
- embedding similarity math
- model “intelligence”

Those concerns belong to **offline evaluation and metrics** (STEP 18).

---

## Design Principle

> The LLM is untrusted.  
> The architecture is the safety boundary.

These tests lock in that boundary.

---

## Maintenance Notes

- Tests use **pytest built-in fixtures only** (`monkeypatch`)
- No dependency on `pytest-mock`
- Do not remove or weaken these tests without updating STEP documentation

---

**Status:** STEP 17 frozen and protected by tests.
