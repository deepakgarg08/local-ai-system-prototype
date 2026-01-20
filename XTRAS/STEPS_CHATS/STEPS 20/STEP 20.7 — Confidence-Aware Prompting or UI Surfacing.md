**Berlin, Germany — 20 January 2026, 20:18 CET**

---

# STEP 20.7 — Confidence-Aware Prompting **and** UI Surfacing

This step answers a very precise question:

> *Now that the system knows its confidence, how do we expose it **without letting the LLM invent or manipulate it**?*

The answer is:
**Confidence is injected *around* the LLM, never *inside its reasoning*.**

---

## Why STEP 20.7 Exists

At the end of STEP 20.6, we had this:

* deterministic confidence: `LOW | MEDIUM | HIGH`
* computed **before** the LLM is called
* grounded in retrieval statistics

But nothing *used* it yet.

### Two big dangers if done wrong

1. ❌ Letting the LLM decide confidence
2. ❌ Hiding confidence until UI (too late for safety)

STEP 20.7 introduces a **controlled surfacing layer**.

---

## Design Decision (Important)

We split this step into **two independent surfaces**:

```
Confidence
   ├── Prompt Surfacing (soft behavioral guidance)
   └── Output Surfacing (hard user-visible signal)
```

This ensures:

* the LLM cannot *change* confidence
* the UI cannot *misinterpret* confidence
* future APIs can reuse the same signal

---

## Folder & File Structure Added

```
pipelines/
├── prompting/
│   └── confidence_prompt.py
│
├── output/
│   └── format_answer.py
│
tests/
├── prompting/
│   └── test_confidence_prompt.py
│
├── output/
│   └── test_answer_formatting.py
│
docs/
└── steps/
    └── step_20_7_confidence_aware_prompting.md
```

Each layer has **exactly one responsibility**.

---

# PART A — Confidence-Aware Prompting (Soft Control)

## Why this exists

We want the LLM to:

* be cautious when confidence is LOW
* be neutral when MEDIUM
* be direct when HIGH

But:

* ❌ no probabilities
* ❌ no self-evaluation
* ❌ no “I think I’m 80% confident”

---

## `pipelines/prompting/confidence_prompt.py`

```python
from pipelines.confidence.calibrate import ConfidenceLevel


def confidence_instruction(confidence: ConfidenceLevel) -> str:
    """
    Returns an instruction string that subtly guides the LLM's tone
    without revealing numeric confidence or allowing self-assessment.
    """

    if confidence == ConfidenceLevel.HIGH:
        return (
            "The retrieved context is strong and unambiguous. "
            "Answer clearly and directly, citing the provided information."
        )

    if confidence == ConfidenceLevel.MEDIUM:
        return (
            "The retrieved context is partially relevant. "
            "Answer carefully and avoid overgeneralization."
        )

    return (
        "The retrieved context is weak or limited. "
        "Do not speculate. If the context is insufficient, say that explicitly."
    )
```

---

### Why this file exists

| Aspect        | Reason                            |
| ------------- | --------------------------------- |
| Separate file | Prompt logic stays centralized    |
| No numbers    | Confidence already decided        |
| No LLM logic  | Pure string policy                |
| Tone-based    | Prevents hallucination escalation |

This is **behavior shaping**, not control flow.

---

## Test — `tests/prompting/test_confidence_prompt.py`

```python
from pipelines.prompting.confidence_prompt import confidence_instruction
from pipelines.confidence.calibrate import ConfidenceLevel


def test_high_confidence_instruction():
    text = confidence_instruction(ConfidenceLevel.HIGH)
    assert "strong and unambiguous" in text


def test_medium_confidence_instruction():
    text = confidence_instruction(ConfidenceLevel.MEDIUM)
    assert "partially relevant" in text


def test_low_confidence_instruction():
    text = confidence_instruction(ConfidenceLevel.LOW)
    assert "Do not speculate" in text
```

---

# PART B — Confidence UI / Output Surfacing (Hard Signal)

## Why this must be separate

Prompting:

* affects *generation*

Output formatting:

* affects *user trust*

Never mix the two.

---

## `pipelines/output/format_answer.py`

```python
from dataclasses import dataclass
from pipelines.confidence.calibrate import ConfidenceLevel


@dataclass(frozen=True)
class FormattedAnswer:
    answer: str
    confidence: ConfidenceLevel
    disclaimer: str | None = None


def format_answer(
    answer: str,
    confidence: ConfidenceLevel,
) -> FormattedAnswer:
    """
    Attach confidence metadata for UI or API layers.
    """

    disclaimer = None

    if confidence == ConfidenceLevel.LOW:
        disclaimer = (
            "⚠️ The available documents do not provide strong support "
            "for a definitive answer. Please verify manually."
        )

    return FormattedAnswer(
        answer=answer,
        confidence=confidence,
        disclaimer=disclaimer,
    )
```

---

### Why this file exists

| Feature                 | Purpose           |
| ----------------------- | ----------------- |
| `FormattedAnswer`       | Structured output |
| Confidence as enum      | No free text      |
| Disclaimer only for LOW | Avoid noise       |
| No UI code              | UI-agnostic       |

This works for:

* CLI
* REST API
* Web UI
* Logging

---

## Test — `tests/output/test_answer_formatting.py`

```python
from pipelines.output.format_answer import format_answer
from pipelines.confidence.calibrate import ConfidenceLevel


def test_low_confidence_adds_disclaimer():
    result = format_answer("Some answer", ConfidenceLevel.LOW)
    assert result.disclaimer is not None


def test_high_confidence_no_disclaimer():
    result = format_answer("Some answer", ConfidenceLevel.HIGH)
    assert result.disclaimer is None
```

---

# Documentation — `docs/steps/step_20_7_confidence_aware_prompting.md`

```md
# STEP 20.7 — Confidence-Aware Prompting & Surfacing

This step integrates confidence signals into both:
- prompt behavior (soft control)
- answer output (hard signal)

Confidence is computed externally and is never generated or modified
by the language model.

## Goals
- Reduce hallucination risk
- Improve user trust
- Support human-in-the-loop workflows

## Non-Goals
- No probabilistic claims
- No LLM self-confidence
- No UI coupling
```

---

## Final End-to-End Flow (Updated)

```
query
  → retrieve
  → rerank
  → gate
  → calibrate_confidence
  → confidence_instruction
  → assemble_prompt
  → LLM
  → format_answer
```

At this point:

✅ The system **knows when it is unsure**
✅ The LLM **behaves accordingly**
✅ The user **can see uncertainty**
✅ The architecture remains clean

---

## What STEP 20.x Achieved Overall

STEP 20 transformed the system from:

> *“It answers questions”*

into:

> *“It answers questions responsibly.”*

---

### Next logical steps (choose one)

* **STEP 21 — Confidence Telemetry & Logging**
* **STEP 22 — Per-Document / Per-Section Confidence**
* **STEP 23 — Confidence-Driven Human Review Workflow**

Tell me which one you want next.
