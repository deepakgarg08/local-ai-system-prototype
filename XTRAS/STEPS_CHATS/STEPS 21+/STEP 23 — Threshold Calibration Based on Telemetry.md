**Berlin, Germany — 1 February 2026, 13:02 CET**

Here is a **clean, honest, freeze-ready summary of STEP 23**, grounded in what your telemetry *actually showed* (not what we hoped it would show).

---

# **STEP 23 — Threshold Calibration Based on Telemetry (SUMMARY)**

## Goal

Derive **defensible similarity thresholds** for grounding decisions using **real system telemetry**, rather than intuition or hard-coded values.

STEP 23 evaluates whether the system’s retrieval quality and model behavior allow a **safe cutoff** between answering and refusing (`IDK`).

---

## Inputs

* Confidence telemetry emitted in **STEP 21**
* Drift patterns observed in **STEP 22**
* A controlled calibration question set (in-scope, borderline, out-of-scope)

No pipeline logic was modified during this step.

---

## What Was Done

1. Executed a representative calibration query set end-to-end
2. Logged:

   * retrieval similarity
   * answer type (ANSWER / IDK)
   * confidence level
   * execution status
3. Analyzed:

   * similarity distributions for ANSWER vs IDK
   * false positives (answers on weak retrieval)
   * model-dependent behavior

---

## Key Findings

### 1. No Safe Threshold Could Be Justified

Across the calibration data:

* A large fraction of `ANSWER` events occurred at **very low similarity**
* Raising similarity thresholds would reject too many existing answers
* Lowering thresholds would allow hallucinations

**Result:**

> No similarity threshold met the safety criteria.

This outcome is correct and intentional.

---

### 2. Model Choice Strongly Affects Grounding Safety

Telemetry revealed clear differences:

* **DeepSeek**

  * answered confidently on missing facts
  * hallucinated out-of-scope answers (e.g. CEO, penalties)
  * ignored weak retrieval signals
* **SmolLM (small models)**

  * far more conservative
  * aligned answer behavior with retrieval quality
  * predictable IDK behavior

This confirmed that **model behavior can invalidate threshold calibration**.

---

### 3. Telemetry Correctly Exposed Unsafe Behavior

STEP 23 validated that:

* unsafe answers were observable
* violations were measurable
* calibration refused to proceed under risk

This proves the **telemetry-first design works**.

---

## What STEP 23 Explicitly Did *Not* Do

* Did not change `MIN_SIMILARITY_THRESHOLD`
* Did not enforce any new gates
* Did not tune confidence scoring
* Did not “fix” model behavior

STEP 23 is **diagnostic, not corrective**.

---

## Outcome

* Threshold calibration **blocked itself** due to safety concerns
* This prevented baking unsafe assumptions into the system
* The system correctly chose **refusal over false confidence**

This is a **successful outcome**, not a failure.

---

## Architectural Insight

> **Thresholds are meaningless if the model violates grounding.**

Calibration is only valid once:

* model behavior is conservative
* hallucinations are structurally blocked

This naturally leads to the next step.

---

## Status

✅ **STEP 23 COMPLETE**
❄️ **FROZEN (NO THRESHOLD CHANGES APPLIED)**

➡️ **Next: STEP 24 — Enforced Thresholds & Deterministic IDK**

---

### One-Line Takeaway

> **STEP 23 proved that similarity thresholds cannot be safely calibrated until grounding violations are structurally prevented — and it correctly refused to guess.**

If you want, I can also:

* compress this into a **changelog entry**, or
* write a **technical justification note** explaining *why no threshold was chosen*
