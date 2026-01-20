**📅 19 January 2026, 16:25 CET (Berlin, Germany)**

Below is a **complete, documentation-ready summary of STEP 20.5 — Score-Aware Answer Gating**, written in the same style as your earlier step summaries.

---

# STEP 20.5 — Score-Aware Answer Gating

## Purpose of This Step

STEP 20.5 introduces a **deterministic safety gate** that decides **whether the system is allowed to generate an answer at all**, based on **rerank scores** produced by the cross-encoder (STEP 20.3).

If the retrieved evidence is **too weak**, the system:

* does **not** call the LLM
* returns **`answer=None` / “I don’t know”**
* still provides **confidence and sources** for explainability

This step marks the transition from:

> *“RAG that can answer”*
> to
> **“RAG that knows when it must not answer.”**

---

## Why This Step Is Necessary

Before STEP 20.5:

* Relevance was computed (similarity + reranking)
* Scores were visible in the prompt (STEP 20.4)
* But **nothing enforced them**

This allowed:

* Answers based on marginal context
* Confident hallucinations
* Violations of the “document-grounded assistant” guarantee

STEP 20.5 fixes this by ensuring:

> **No LLM call happens unless evidence quality meets a minimum standard.**

---

## Architectural Principle

**Answer gating is policy, not ML.**

* ❌ The LLM must never decide whether it should answer
* ❌ Rerank scores must not implicitly become truth
* ✅ A deterministic system rule decides

This preserves:

* auditability
* safety
* explainability
* legal and operational defensibility

---

## New Folder Structure

```
pipelines/
└── gating/
    ├── __init__.py
    ├── base.py
    ├── score_gate.py
    └── gate.py
```

### Why a new `gating/` pipeline?

Because gating is **neither retrieval, nor reranking, nor prompting**.
It is a **control-flow decision layer**.

---

## Files Created (with Purpose and Code)

---

### `pipelines/gating/__init__.py`

```python
# Answer gating pipeline.
# Contains policies that decide whether the system is allowed to generate an answer.
```

---

### `pipelines/gating/base.py`

**Purpose:**
Defines the abstract contract for all gating strategies.

```python
# Defines the abstract contract for answer gating.
# Gates decide whether an LLM is allowed to generate an answer.

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseGate(ABC):
    @abstractmethod
    def allow_answer(self, chunks: List[Dict]) -> bool:
        """
        Return True if an answer is allowed, False otherwise.
        """
        raise NotImplementedError
```

---

### `pipelines/gating/score_gate.py`

**Purpose:**
Implements a deterministic gate based on **rerank scores**.

```python
# Implements score-based answer gating.
# Blocks LLM calls when reranked evidence is too weak.

from typing import List, Dict

from pipelines.gating.base import BaseGate


class ScoreThresholdGate(BaseGate):
    def __init__(self, min_score: float):
        self.min_score = min_score

    def allow_answer(self, chunks: List[Dict]) -> bool:
        if not chunks:
            return False

        best_score = max(
            chunk.get("rerank_score", 0.0) for chunk in chunks
        )

        return best_score >= self.min_score
```

---

### `pipelines/gating/gate.py`

**Purpose:**
Orchestrates gating policy and injects runtime configuration
(keeps thresholds out of core logic).

```python
# Orchestrates answer gating policies.
# Threshold is loaded from runtime configuration (not hard-coded).

from typing import List, Dict

from pipelines.gating.score_gate import ScoreThresholdGate
from configs.runtime import RERANK_MIN_SCORE


def is_answer_allowed(chunks: List[Dict]) -> bool:
    gate = ScoreThresholdGate(min_score=RERANK_MIN_SCORE)
    return gate.allow_answer(chunks)
```

---

## Configuration Added / Updated

### `configs/runtime.py` (updated)

**Purpose:**
Expose gating threshold as **policy-level configuration**, not code.

```python
# STEP 20.5 — policy-level threshold for answer gating
RERANK_MIN_SCORE: float = _get_float_env("RERANK_MIN_SCORE", 0.5)
```

This allows:

* tuning without code changes
* environment-specific behavior
* safe defaults

---

## Integration Point

### `pipelines/query/run_rag.py`

**Where gating happens:**

```
retrieve
→ rerank
→ SCORE-AWARE GATE (STEP 20.5)
→ assemble prompt
→ LLM
```

If the gate fails:

* LLM is never called
* answer is blocked deterministically

---

## Test Files Created

```
tests/
└── gating/
    └── test_score_gate.py
```

---

### `tests/gating/test_score_gate.py`

```python
# Tests score-based answer gating behavior.
# Ensures weak evidence blocks answers deterministically.

from pipelines.gating.score_gate import ScoreThresholdGate


def test_allows_answer_when_score_is_high():
    gate = ScoreThresholdGate(min_score=0.5)

    chunks = [
        {"text": "A", "rerank_score": 0.82},
        {"text": "B", "rerank_score": 0.40},
    ]

    assert gate.allow_answer(chunks) is True


def test_blocks_answer_when_score_is_low():
    gate = ScoreThresholdGate(min_score=0.5)

    chunks = [
        {"text": "A", "rerank_score": 0.31},
        {"text": "B", "rerank_score": 0.42},
    ]

    assert gate.allow_answer(chunks) is False


def test_blocks_answer_when_no_chunks():
    gate = ScoreThresholdGate(min_score=0.5)

    assert gate.allow_answer([]) is False
```

These tests guarantee:

* deterministic behavior
* no silent regressions
* safety logic remains intact

---

## What This Step Explicitly Does *Not* Do

STEP 20.5 does **not**:

* change retrieval behavior
* change reranking behavior
* involve the LLM in safety decisions
* interpret or explain scores

It only answers one question:

> **“Is the evidence strong enough to allow an answer?”**

---

## Outcome of STEP 20.5

| Capability                    | Status |
| ----------------------------- | ------ |
| Deterministic answer blocking | ✅      |
| Hallucination prevention      | ✅      |
| Policy separated from ML      | ✅      |
| LLM safety enforced           | ✅      |
| Configurable thresholds       | ✅      |

This step upgrades the system from **best-effort RAG** to a **trust-aware, safety-first assistant**.

---

### Next Logical Step

👉 **STEP 20.6 — Confidence Calibration (LOW / MEDIUM / HIGH)**
Derive confidence labels from real signals, not from the LLM.

When ready, just say **STEP 20.6**.


**📅 19 January 2026, 15:47 CET (Berlin, Germany)**

Short answer: **yes — they are different things**, even though they are *numerically related*.
Long answer below, because this distinction is **fundamental** to your architecture.

---

## 1️⃣ Rerank score vs Gate score — the core difference

### 🔹 **Rerank score**

* **What it is:**
  A *raw relevance signal* produced by the **cross-encoder**
* **Who produces it:**
  The ML model (`CrossEncoder`)
* **Granularity:**
  Per **(query, chunk)** pair
* **Nature:**
  Continuous, probabilistic, model-dependent

Example:

```python
chunk["rerank_score"] = 0.92
```

Think of it as:

> “How relevant does the model think this chunk is to the query?”

---

### 🔹 **Gate score (or gate decision)**

* **What it is:**
  A *policy decision* derived **from** rerank scores
* **Who produces it:**
  Your **system logic**, not an ML model
* **Granularity:**
  Per **query / answer attempt**
* **Nature:**
  Deterministic, binary (allow / block)

Example:

```python
allow = best_rerank_score >= threshold
```

Think of it as:

> “Is the evidence strong enough to even allow an answer?”

---

## 2️⃣ Important: there is NO separate “gate score” (yet)

Right now, your system does **not** compute a new numeric score called `gate_score`.

Instead:

* It **uses rerank scores as inputs**
* Applies a **rule**
* Produces a **decision**

So technically:

```
rerank_score  ──▶  gate rule  ──▶  allow / deny
```

Not:

```
rerank_score  ──▶  gate_score  ──▶  allow / deny
```

That distinction is intentional and **good design**.

---

## 3️⃣ Why keeping them separate matters

### ❌ Bad design (conflation)

If you treated rerank score *as* the gate:

* ML behavior becomes policy
* Model changes silently alter system guarantees
* Auditing becomes impossible

Example of what you are **avoiding**:

> “The model decided not to answer.”

That’s unacceptable in serious systems.

---

### ✅ Good design (what you have)

You can say:

* “The **model** estimated relevance”
* “The **system** decided whether to answer”

This gives you:

* Accountability
* Explainability
* Tunability
* Legal & operational defensibility

---

## 4️⃣ Mental model (very important)

Use this rule of thumb:

> **Rerank score = evidence signal**
> **Gate decision = safety policy**

Or more concretely:

| Layer    | Question it answers                  |
| -------- | ------------------------------------ |
| Reranker | “How relevant is this chunk?”        |
| Gate     | “Is relevance sufficient to answer?” |
| LLM      | “How do I phrase the answer?”        |

Each layer answers **one question only**.

---

## 5️⃣ Will there ever be a “gate score”?

Possibly — **later**, and only if justified.

For example:

* Combine:

  * best rerank score
  * score gap (top1 − top2)
  * number of strong chunks
* Produce an *aggregated confidence signal*

That might look like:

```python
gate_confidence = f(rerank_scores)
```

But even then:

* The **gate** owns that logic
* The **LLM never does**

You are **not there yet**, and that’s correct.

---

## 6️⃣ Why your question shows good instincts

You’re implicitly asking:

> “Are we accidentally letting ML outputs become system truth?”

And the answer is:

➡️ **No — because you explicitly separated them.**

That’s exactly the difference between:

* a demo RAG
* and a production-grade, auditable system

---

## ✅ Final, crisp answer

* **Rerank score:** model-generated relevance signal (per chunk)
* **Gate score:** ❌ does not exist as a raw number
* **Gate decision:** system-level policy derived from rerank scores

They are **not the same**, and **must never be conflated**.

---

If you want, the next clean continuation is:

👉 **STEP 20.6 — Confidence Calibration**
(where we *derive* LOW / MEDIUM / HIGH **without** letting the LLM decide)

Just say the step number.
