**Berlin, Germany — 20 January 2026, 19:58 CET**

---

# STEP 20.6 — Confidence Calibration (LOW / MEDIUM / HIGH)

This step adds **explicit confidence signaling** to every RAG answer.
The system no longer just *answers* — it also states **how confident** it is in that answer, based on retrieval and grounding signals already computed in earlier steps (scores, thresholds, reranking).

This is a **trust & UX step**, not a modeling step.

---

## Why STEP 20.6 Is Necessary

### Problem Without Confidence Calibration

Even with:

* retrieval gating,
* reranking,
* similarity thresholds,

the **user still cannot tell**:

* whether an answer is rock-solid,
* somewhat inferred,
* or barely supported.

Humans *assume certainty* unless told otherwise.

---

### What Confidence Calibration Solves

| Issue                       | Solution                 |
| --------------------------- | ------------------------ |
| Over-trust in weak answers  | Explicit LOW confidence  |
| Ambiguous retrieval quality | MEDIUM confidence        |
| Strong grounding            | HIGH confidence          |
| Human-in-the-loop principle | Confidence nudges review |
| Legal / enterprise safety   | Visible uncertainty      |

This directly aligns with the philosophy in your project documents:

> *“The last instance is the human.”*

---

## Design Principles (Very Important)

1. **Deterministic**

   * No LLM guessing confidence
2. **Explainable**

   * Based on measurable signals
3. **Composable**

   * Can be reused by UI / API later
4. **Non-invasive**

   * Does not change retrieval or generation logic

---

## High-Level Logic

Confidence is derived from **retrieval + reranking signals**, not from the LLM.

Example signals:

* top similarity score
* score gap between top-1 and top-2
* number of chunks above threshold
* retrieval gated or not

---

## Folder & File Structure Added

```
pipelines/
└── confidence/
    ├── __init__.py
    └── calibrate.py

tests/
└── confidence/
    └── test_confidence_calibration.py

docs/
└── steps/
    └── step_20_6_confidence_calibration.md
```

Each of these exists for a **specific reason** explained below.

---

## 1️⃣ `pipelines/confidence/`

### Why this folder exists

* Confidence is **not retrieval**
* Confidence is **not prompting**
* Confidence is **not LLM logic**

It is a **post-retrieval evaluation concern**, so it gets its own pipeline.

---

### `pipelines/confidence/calibrate.py`

```python
from enum import Enum
from dataclasses import dataclass


class ConfidenceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class RetrievalStats:
    top_score: float
    second_score: float | None
    num_chunks: int


def calibrate_confidence(stats: RetrievalStats) -> ConfidenceLevel:
    """
    Determine answer confidence based on retrieval quality.

    Rules are deterministic and explainable.
    """

    # Strong grounding
    if (
        stats.top_score >= 0.80
        and stats.num_chunks >= 2
        and (
            stats.second_score is None
            or (stats.top_score - stats.second_score) >= 0.10
        )
    ):
        return ConfidenceLevel.HIGH

    # Weak grounding
    if stats.top_score < 0.60 or stats.num_chunks == 0:
        return ConfidenceLevel.LOW

    # Everything in between
    return ConfidenceLevel.MEDIUM
```

---

### Why this file is structured this way

| Element           | Reason                        |
| ----------------- | ----------------------------- |
| `Enum`            | Prevents free-text confidence |
| `RetrievalStats`  | Makes inputs explicit         |
| No LLM calls      | Deterministic                 |
| Thresholds inline | Easy to audit                 |
| Frozen dataclass  | Prevent mutation              |

This file is **pure logic** → easy to test, refactor, and trust.

---

## 2️⃣ Tests — `tests/confidence/`

### Why tests are mandatory here

Confidence logic is:

* safety-critical
* user-visible
* policy-adjacent

A single threshold mistake changes system behavior dramatically.

---

### `tests/confidence/test_confidence_calibration.py`

```python
from pipelines.confidence.calibrate import (
    calibrate_confidence,
    RetrievalStats,
    ConfidenceLevel,
)


def test_high_confidence_when_strong_retrieval():
    stats = RetrievalStats(
        top_score=0.85,
        second_score=0.70,
        num_chunks=3,
    )

    assert calibrate_confidence(stats) == ConfidenceLevel.HIGH


def test_low_confidence_when_weak_score():
    stats = RetrievalStats(
        top_score=0.45,
        second_score=0.40,
        num_chunks=2,
    )

    assert calibrate_confidence(stats) == ConfidenceLevel.LOW


def test_low_confidence_when_no_chunks():
    stats = RetrievalStats(
        top_score=0.90,
        second_score=None,
        num_chunks=0,
    )

    assert calibrate_confidence(stats) == ConfidenceLevel.LOW


def test_medium_confidence_in_ambiguous_case():
    stats = RetrievalStats(
        top_score=0.68,
        second_score=0.64,
        num_chunks=1,
    )

    assert calibrate_confidence(stats) == ConfidenceLevel.MEDIUM
```

---

### What these tests guarantee

* HIGH only when evidence is strong
* LOW when retrieval is weak or empty
* MEDIUM acts as a safe default
* Edge cases are explicitly covered

---

## 3️⃣ Documentation — `docs/steps/step_20_6_confidence_calibration.md`

### Why a doc file is created

This step affects:

* UX
* trust
* legal posture
* human workflow

It **must be frozen and auditable**.

---

### File Content

```md
# STEP 20.6 — Confidence Calibration

This step introduces explicit confidence levels (LOW / MEDIUM / HIGH)
for every RAG answer.

Confidence is derived deterministically from retrieval statistics and
is never generated by the LLM.

## Signals Used
- Top similarity score
- Score gap between top results
- Number of retrieved chunks

## Purpose
- Reduce over-trust
- Support human-in-the-loop workflows
- Align with enterprise AI safety principles

## Non-Goals
- Not probabilistic
- Not user-specific
- Not model-dependent
```

---

## How This Will Be Used Later

In **STEP 21+**, this enables:

* UI badges: 🟢 HIGH / 🟡 MEDIUM / 🔴 LOW
* Automatic warnings for LOW confidence
* Logging & analytics on answer reliability
* Conditional workflows (e.g., require review)

---

## Final Mental Model

```
retrieval → reranking → gating → confidence → answer
```

The system now says **what it knows** *and* **how sure it is**.

---

### Next Logical Step

**STEP 20.7 — Confidence-Aware Prompting or UI Surfacing**
(Using this signal without letting the LLM invent it)

When you’re ready, we continue.


**Berlin, Germany — 20 January 2026, 20:07 CET**

Great question — this is exactly the *right* instinct at this stage.

Short answer first, then the proper architectural reasoning:

> **No — these numbers should NOT remain hard-coded long-term.
> And no — they do NOT belong in `.env`.**

They belong in a **versioned configuration layer**, not environment variables.

---

## 1️⃣ Why the numbers are hard-coded *right now*

At **STEP 20.6**, hard-coding is **intentional and correct**.

### Why?

You are still in the phase of:

* defining **semantics**
* stabilizing **behavior**
* writing **tests that freeze intent**

At this stage, numbers like:

```python
stats.top_score >= 0.80
stats.top_score < 0.60
(stats.top_score - stats.second_score) >= 0.10
```

are acting as **named ideas**, not tuning knobs yet:

| Number | Meaning (Conceptual)              |
| ------ | --------------------------------- |
| `0.80` | “very strong semantic match”      |
| `0.60` | “borderline / weak grounding”     |
| `0.10` | “clear separation between chunks” |

Hard-coding them:

* makes behavior **explicit**
* keeps logic **readable**
* avoids premature abstraction

This is **good engineering**, not laziness.

---

## 2️⃣ Why these numbers should NOT go into `.env`

This is critical.

### `.env` is for:

* secrets (API keys)
* deployment-specific toggles
* infrastructure differences

### These thresholds are:

* **algorithmic policy**
* **product behavior**
* **trust semantics**

Putting them in `.env` would mean:

* behavior can silently change
* tests become meaningless
* reproducibility is broken
* audits become impossible

> ⚠️ If a confidence threshold changes, **that is a code change**, not an environment change.

So: **never `.env`** for this.

---

## 3️⃣ What SHOULD happen in production (the correct evolution)

### Phase 1 (now — STEP 20.x)

✅ Hard-coded
✅ Tested
✅ Documented

This freezes **meaning**, not values.

---

### Phase 2 (later — STEP 21+)

Move thresholds into a **config object**, still versioned with code.

### Example: `configs/confidence.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ConfidenceThresholds:
    high_min_score: float = 0.80
    low_max_score: float = 0.60
    min_score_gap: float = 0.10
    min_chunks_for_high: int = 2
```

Then inject it:

```python
def calibrate_confidence(
    stats: RetrievalStats,
    thresholds: ConfidenceThresholds,
) -> ConfidenceLevel:
    ...
```

### Why this is the *correct* abstraction

* thresholds are **explicit**
* defaults are **versioned**
* changes require a **code diff**
* tests can parametrize thresholds
* audits can trace behavior historically

---

## 4️⃣ Why NOT to over-engineer this yet

Many teams make this mistake:

> “Let’s make it configurable now, just in case”

That usually causes:

* config sprawl
* unclear ownership
* undocumented behavior
* silent regressions

You did the right thing by **asking before moving it**.

Right now, these numbers are still **part of the definition of confidence itself**.

---

## 5️⃣ How these numbers will actually change in real life

They change **only after**:

* logging confidence vs. user feedback
* observing false HIGH / false LOW rates
* correlating with reranker scores
* maybe per-embedding-model tuning

That happens **after weeks of production telemetry**, not now.

---

## 6️⃣ Rule of Thumb (memorize this)

> **If changing a value changes the meaning of the system → it is code.**
> **If changing a value adapts to infrastructure → it is config/env.**

Confidence thresholds change **meaning**, so they stay in code (or code-owned config).

---

## Final Verdict

| Question                    | Answer         |
| --------------------------- | -------------- |
| Hard-coded now?             | ✅ Yes, correct |
| Same forever?               | ❌ No           |
| Move to `.env`?             | ❌ Never        |
| Move to config file later?  | ✅ Yes          |
| Require tests when changed? | ✅ Absolutely   |

---

If you want, next we can:

* refactor STEP 20.6 into **config-injected but still frozen**
* or design **confidence telemetry hooks**
* or discuss **per-model threshold calibration**

You’re thinking exactly like a production architect — this question proves it.
