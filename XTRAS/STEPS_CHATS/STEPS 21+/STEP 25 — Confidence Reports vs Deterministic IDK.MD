**Berlin, Germany — 1 February 2026, 15:02 CET**

---

# **STEP 25 — Confidence Reports vs Deterministic IDK**

STEP 25 is **not** about “adding a confidence score to answers”.
It is about **separating two fundamentally different outcomes**:

> **“We cannot answer”**
> vs
> **“We can answer, but only with bounded confidence”**

This distinction is *explicitly required* by the project’s philosophical and contractual foundations .

---

## 1. Why STEP 25 Exists (Conceptually)

From STEP 24, your system already does this:

* ❌ blocks hallucinations
* ❌ blocks weak retrieval
* ✅ returns deterministic IDK

But STEP 24 is **binary**:

```
answer OR IDK
```

That is safe — but **too coarse** for real usage.

STEP 25 introduces a **third state**:

```
IDK
LOW-CONFIDENCE ANSWER (WITH REPORT)
HIGH-CONFIDENCE ANSWER (WITH REPORT)
```

Crucially:

* **IDK remains system-decided**
* **Confidence is explanatory, not permissive**

---

## 2. Non-Negotiable Rule (Anchor This)

> **Confidence NEVER overrides IDK.**

If STEP 24 blocks → STEP 25 is not executed.

This aligns directly with the document’s core axiom:

> *„Die letzte Instanz ist der Mensch.“* 

Confidence exists **for the human**, not for the model.

---

## 3. What “Confidence” Means in *Your* Architecture

In your system, confidence is **not**:

* model self-confidence
* logprobs
* “I’m 80% sure”

Instead, it is a **retrieval-grounding report**.

### Confidence is derived from:

* retrieval scores
* score distribution
* chunk count
* document coverage
* ambiguity signals

All of these already exist or proto-exist in:

```text
pipelines/query/confidence.py
```

STEP 25 **formalizes** that file.

---

## 4. Outcome Types (Conceptual)

After STEP 25, every query results in **exactly one** of:

### 1️⃣ Deterministic IDK

*(from STEP 24)*

Returned when:

* relevance gate fails
* ambiguity too high
* grounding insufficient

No confidence report needed.

---

### 2️⃣ Answer + Confidence Report

Returned when:

* relevance gate passes
* but uncertainty is non-zero (almost always)

Structure (conceptual):

```text
ANSWER
---
Confidence summary:
• Source documents: 3
• Strongest similarity: 0.91
• Coverage: partial
• Ambiguities detected: yes
```

This is **not optional UX sugar** — it is a **trust artifact**.

---

## 5. Why This Is Required by the Contract

Your Leistungsbeschreibung repeatedly stresses:

* probabilistic nature of KI
* hallucination risk
* mandatory human validation
* no liability for decisions based on outputs 

STEP 25 is how you **encode those statements into behavior**.

Without STEP 25:

* the system *looks* authoritative
* users over-trust outputs

With STEP 25:

* uncertainty is visible
* responsibility is explicit
* the human is forced to evaluate

This is exactly what the document demands.

---

## 6. Relationship Between STEP 24 and STEP 25

Think in layers:

```
STEP 24 → Can we answer at all?
STEP 25 → How reliable is the answer we give?
```

| Layer   | Role                             |
| ------- | -------------------------------- |
| STEP 24 | Safety gate (hard stop)          |
| STEP 25 | Transparency layer (explanation) |

They must **never be merged**.

---

## 7. Where This Lives (Given Your Existing Structure)

Based on your current project (as recalled correctly):

```text
pipelines/query/
├── retriever.py
├── run_rag.py
├── confidence.py        ← THIS becomes formalized
├── validation/          ← STEP 24
│   └── relevance_gate.py
├── fallbacks/
│   └── idk.py
```

STEP 25 **does not add new folders**.

It:

* upgrades `confidence.py`
* wires it into `run_rag.py`
* ensures it never runs on IDK paths

---

## 8. What STEP 25 Is *Not*

Very important to avoid future drift:

❌ Not model calibration
❌ Not probability of correctness
❌ Not user-facing “trust score”
❌ Not LLM self-evaluation

✅ It is **retrieval-grounding explainability**

---

## 9. Canonical One-Line Definition

> **STEP 25 introduces structured confidence reports for grounded answers, while preserving deterministic IDK as a hard safety outcome, thereby making uncertainty explicit and human validation unavoidable.**

---

## 10. Natural Next Implementation Steps

If you want to move forward cleanly, the next *implementation* phase would be:

1. Formalize a `ConfidenceReport` structure
2. Make `confidence.py` consume retrieval signals
3. Attach reports only to non-IDK answers
4. Add tests proving:

   * IDK → no confidence
   * confidence never bypasses relevance gate

Say the word, and I’ll do STEP 25 **implementation-grade**, just like we did for STEP 24 — minimal delta, no folder churn, no repetition.

**Berlin, Germany — 1 February 2026, 16:29 CET**

---

## **STEP 25 — Confidence Reports vs IDK (Summary)**

STEP 25 does **not** change when the system answers.
It changes **how uncertainty is represented, exposed, and audited** once that decision is made.

---

### **What STEP 25 Adds**

STEP 25 introduces a **clear semantic separation** between:

1. **System refusal (IDK)**
2. **Answered responses with varying confidence**

This is achieved by attaching a **deterministic confidence report** to every RAG outcome.

---

### **Core Rules Introduced**

1. **Confidence never decides**

   * All answer / no-answer decisions are made in STEP 24 (grounding & gating).
   * Confidence is purely explanatory.

2. **Confidence is retrieval-based**

   * Derived only from retrieval evidence (similarity scores, chunk count, ambiguity).
   * Never influenced by the LLM output.

3. **IDK is not “low confidence”**

   * When the system refuses to answer:

     * `answer = None`
     * internal `confidence_level = "none"`
   * This explicitly encodes *“no answer exists”*, not *“weak answer”*.

4. **Human-in-the-loop is enforced**

   * Every answer is accompanied by visible uncertainty signals.
   * Responsibility for acceptance or rejection remains with the human user.

---

### **Internal vs External Semantics**

* **Internal system semantics**

  * `confidence_level = "none"` is reserved exclusively for IDK.
  * This preserves safety, auditability, and clear system guarantees.

* **External / telemetry semantics**

  * For reporting or dashboards, IDK may be mapped to `LOW` or `MEDIUM`
    without weakening internal correctness.
  * This keeps UX and metrics simple while preserving strong internals.

---

### **What STEP 25 Does *Not* Do**

* Does not introduce new gates or thresholds
* Does not improve answer quality
* Does not calibrate confidence probabilities
* Does not affect LLM behavior

STEP 25 is about **transparency and contract clarity**, not intelligence.

---

### **Why STEP 25 Matters**

Without STEP 25:

* Refusals and weak answers look similar
* Uncertainty is implicit
* Users over-trust outputs

With STEP 25:

* IDK is explicit and machine-readable
* Confidence is visible and explainable
* Telemetry can distinguish refusal vs weak answers
* The system is audit-safe and legally defensible

---

### **One-Line Definition**

> **STEP 25 formalizes uncertainty by attaching deterministic, retrieval-based confidence reports to RAG outputs while preserving IDK as a hard system refusal, making uncertainty explicit and human validation unavoidable.**

---

If you want, the natural next step is **STEP 26 — Confidence calibration & offline evaluation**, where these confidence signals finally start influencing system tuning (not runtime decisions).


**Berlin, Germany — 1 February 2026, 17:09 CET**

---

## **STEP 25 — Explainer Wiring (Summary)**

This final part of STEP 25 ensures that **uncertainty is not only computed, but clearly explained** — especially when the system refuses to answer.

---

### **What Changed in the Explainer**

The explainer (`build_explanation()` in `pipelines/confidence/explainer.py`) was upgraded to **explicitly consume `retrieval_stats`** from `ConfidenceReport`.

Before:

* Explanations were based only on:

  * `confidence_level`
  * number of retrieved chunks
* Different failure modes produced similar explanations

After:

* Explanations are grounded in **structured retrieval facts**, including:

  * `relevance_gate` (e.g. `"FAILED"`)
  * `num_chunks`
  * `max_similarity`

This makes explanations **specific, truthful, and auditable**.

---

### **IDK Is Now Explicitly Explainable**

When the system returns IDK (`answer=None`, `confidence_level="none"`):

* The explainer checks `retrieval_stats["relevance_gate"]`
* If it failed, the explanation clearly states:

  * no sufficiently relevant internal information was found
  * the system therefore did not generate an answer

IDK is no longer a silent or generic failure.

---

### **Answered Responses Are Contextualized**

For non-IDK responses, the explainer now:

* Reports how many chunks were used
* Mentions how many internal documents contributed
* Flags weak semantic similarity when applicable
* Always includes a human-in-the-loop warning

This makes **confidence levels interpretable**, not just labels.

---

### **What the Explainer Does *Not* Do**

* It does **not** influence gating or decisions
* It does **not** introduce thresholds
* It does **not** inspect LLM output
* It does **not** change system behavior

The explainer is **purely explanatory**, by design.

---

### **Why This Matters**

This wiring completes STEP 25 by ensuring:

* Every refusal is explainable
* Every answer is transparent
* Telemetry and audits can trace *why* the system acted as it did
* STEP 26 calibration has reliable, structured inputs

In short:

> **STEP 25 is not complete until uncertainty is both computed *and* explained.**

---

### **One-Line Takeaway**

> **The explainer now turns retrieval statistics into clear, human-readable explanations without influencing decisions, completing STEP 25’s transparency and auditability guarantees.**

You’re now fully ready to move into **STEP 26 — Offline calibration**, where these stats finally begin to influence behavior *outside* the runtime path.
