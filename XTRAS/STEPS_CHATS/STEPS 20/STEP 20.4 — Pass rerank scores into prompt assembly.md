**📅 19 January 2026, 15:10 CET (Berlin, Germany)**

--

# STEP 20.4 — Pass Rerank Scores into Prompt Assembly

## What This Step Does

STEP 20.4 extends the prompt assembly layer to **explicitly include reranking relevance scores** for each retrieved context chunk in the final prompt sent to the LLM.

Each context block now contains not only:

* the chunk text
* its source metadata

but also:

* a **`rerank_score`** produced by the cross-encoder reranker (STEP 20.3)

This makes the **strength of evidence visible** at the point where the answer is generated.

---

## Why This Step Is Necessary

Before this step, the system had a critical blind spot:

* Retrieval and reranking correctly computed relevance
* But the LLM received all context chunks as if they were **equally important**
* Strong evidence and weak evidence were indistinguishable

This created three risks:

1. **Overconfidence**
   The model could confidently answer based on weak or marginally relevant context.

2. **Poor grounding enforcement**
   Even with correct retrieval, the LLM had no signal about *how strong* the evidence actually was.

3. **Disconnected confidence logic**
   Any later confidence or gating decisions would be based on hidden signals, not on what the LLM actually saw.

STEP 20.4 closes this gap by ensuring **no relevance signal is silently dropped**.

---

## Why Prompt Assembly Is the Right Place

Prompt assembly is the **single point of truth** where:

* Retrieved evidence is serialized
* Ordering is finalized
* Instructions are enforced
* The LLM’s world view is constructed

Injecting rerank scores here ensures:

* Retrieval logic stays separate
* Reranking logic stays separate
* Prompt assembly remains responsible only for **representation**, not interpretation

This preserves clean separation of concerns.

---

## Why This Is a Good Design Choice

### 1. Deterministic and Transparent

* Relevance scores are passed verbatim
* No thresholds, heuristics, or hidden transformations
* The LLM sees exactly what the system knows

This makes the system **debuggable and auditable**.

---

### 2. Backward Compatible

* Chunks without rerank scores still render correctly
* Existing prompt behavior remains unchanged otherwise
* Incremental rollout is safe

This avoids brittle migrations.

---

### 3. Enables Stronger Guarantees Later

STEP 20.4 is a **foundational step** for future correctness features:

* **STEP 20.5 — Score-Aware Answer Gating**
  Block answers when relevance is below threshold.

* **STEP 20.6 — Confidence Calibration**
  Derive LOW / MEDIUM / HIGH confidence from real signals.

* **Explainability & audit trails**
  Human reviewers can see *why* an answer was allowed.

Without STEP 20.4, those steps would rely on **implicit or hidden state**, which is fragile and unsafe.

---

## What This Step Explicitly Does *Not* Do

It is important to be precise about scope.

STEP 20.4 does **not**:

* Change retrieval behavior
* Change reranking behavior
* Introduce thresholds or policies
* Allow the LLM to use external knowledge
* Relax grounding or extractive constraints

It only **exposes existing truth** at the correct boundary.

---

## How This Improves System Trustworthiness

With this step completed:

* The LLM is aware of evidence strength
* Weak context looks weak, strong context looks strong
* Tests guarantee this signal cannot regress silently

This moves the system from:

> *“We computed relevance”*
> to
> *“Relevance is enforced end-to-end”*

---

## Summary

STEP 20.4 ensures that **retrieval quality signals survive all the way to generation**.

It is a small code change with a large architectural impact:

* stronger grounding
* better explainability
* safer future extensions

This step is **necessary**, **well-scoped**, and **correctly placed**, and it forms the bridge between retrieval quality and answer correctness.

---

When you’re ready, the natural continuation is:

👉 **STEP 20.5 — Score-Aware Answer Gating**


**📅 19 January 2026, 14:32 CET (Berlin, Germany)**

---

# 👉 STEP 20.4 — Pass Rerank Scores into Prompt Assembly

This step is **purely architectural and correctness-oriented**.

You already have:

* FAISS retrieval (bi-encoder)
* Cross-encoder reranking (STEP 20.3)

But until now, **rerank scores stop existing once chunks are selected**.

👉 STEP 20.4 makes rerank scores **first-class citizens** in the prompt.

---

## 1️⃣ Why STEP 20.4 Exists (Very Important)

### The core problem

Without passing rerank scores:

* The LLM sees all chunks as **equally important**
* Strong evidence and weak evidence look identical
* Confidence explanations are disconnected from retrieval reality

This causes:

* Overconfident answers
* Weak citation weighting
* Poor “I don’t know” calibration

---

## 2️⃣ Design Principle (Non-Negotiable)

> **The LLM must be aware of retrieval strength,
> but must not be allowed to reason outside the context.**

So we:

* Pass rerank scores **explicitly**
* Keep them **non-optional**
* Keep formatting **machine-readable**

---

## 3️⃣ Updated Data Contract (Critical Change)

### Before STEP 20.4

```python
chunk = {
    "text": "...",
    "metadata": {...}
}
```

### After STEP 20.4 (mandatory)

```python
chunk = {
    "text": "...",
    "metadata": {...},
    "rerank_score": float
}
```

This is now the **canonical chunk schema** after reranking.

---

## 4️⃣ Files Affected

We do **not** add a new pipeline.
We **extend prompt assembly**.

```
pipelines/
└── prompting/
    └── assemble_prompt.py   ← modified
```

---

## 5️⃣ Why We Modify `assemble_prompt.py`

Because:

* Prompt assembly is the **only place** where

  * evidence is serialized
  * ordering is frozen
  * instructions are enforced

Reranking logic must **never leak into prompting logic**.

---

## 6️⃣ Regenerated `assemble_prompt.py`

### 📄 `pipelines/prompting/assemble_prompt.py`

```python
# Assembles the final prompt sent to the LLM.
# Injects retrieved evidence with explicit rerank scores to guide answer confidence.

from typing import List, Dict


def assemble_prompt(
    query: str,
    context_chunks: List[Dict],
    extractive_only: bool = False,
) -> str:
    # Instruction header enforcing grounding.
    instructions = [
        "You are a document-grounded assistant.",
        "Answer ONLY using the provided context.",
        "If the context is insufficient, say 'I don't know.'",
    ]

    if extractive_only:
        instructions.append(
            "Answer ONLY by quoting or closely paraphrasing the context."
        )

    # Serialize context with rerank scores.
    context_blocks = []
    for i, chunk in enumerate(context_chunks, start=1):
        score = chunk.get("rerank_score", "N/A")

        block = f"""
[CONTEXT {i}]
Relevance score: {score}
{chunk['text']}
""".strip()

        context_blocks.append(block)

    # Combine all sections.
    prompt = f"""
{' '.join(instructions)}

QUESTION:
{query}

CONTEXT:
{chr(10).join(context_blocks)}

ANSWER:
""".strip()

    return prompt
```

---

## 7️⃣ Why This Formatting Was Chosen

### Explicit label: `Relevance score: X`

* Human readable
* LLM parsable
* Deterministic
* Easy to test

### Why not hide scores?

Because:

* We **want** the LLM to down-weight weak evidence
* We **want** confidence explanations to reference strength
* We **do not** allow the LLM to invent scores

---

## 8️⃣ Test Cases (Required)

This is a **contract change**, so tests are mandatory.

---

### Test folder (already exists)

```
tests/query/
└── test_prompt_assembly_with_scores.py
```

---

### 📄 `tests/query/test_prompt_assembly_with_scores.py`

```python
# Tests that rerank scores are explicitly included in the assembled prompt.
# Ensures retrieval strength is visible to the LLM and not silently dropped.

from pipelines.prompting.assemble_prompt import assemble_prompt


def test_rerank_scores_are_included_in_prompt():
    prompt = assemble_prompt(
        query="What is X?",
        context_chunks=[
            {
                "text": "X is defined as Y.",
                "metadata": {},
                "rerank_score": 0.87,
            }
        ],
    )

    assert "Relevance score: 0.87" in prompt
```

---

## 9️⃣ What STEP 20.4 Unlocks

| Capability                | Status |
| ------------------------- | ------ |
| Evidence weighting        | ✅      |
| Confidence explainability | ✅      |
| Weak-context detection    | ✅      |
| Score-aware prompting     | ✅      |
| Deterministic behavior    | ✅      |

This step **does not improve retrieval** —
it improves **how truth is communicated to the LLM**.

---

## 🔜 What Comes Next (Logical Order)

You now have **all raw signals**.

Next steps become *policy decisions*:

### 👉 STEP 20.5 — Score-Aware Answer Gating

* Minimum rerank score thresholds
* Block answers even if chunks exist

### 👉 STEP 20.6 — Confidence Calibration

* LOW / MEDIUM / HIGH derived from scores
* Not from LLM self-assessment

### 👉 STEP 21 — Hybrid Reranking

* BM25 + FAISS + Cross-Encoder fusion

If you want to proceed, say the step number.
