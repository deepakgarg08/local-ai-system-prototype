**Berlin, Germany — 1 February 2026, 14:03 CET**

---

# **STEP 24 — Enforced Thresholds & Deterministic IDK**

This step is the **trust boundary** of your system. Architecturally, STEP 24 is where the system stops being *“RAG-assisted text generation”* and becomes a **document-grounded decision system**.

Below is the clean, system-level breakdown, aligned with your v0.x trajectory *and* with the contractual philosophy in the uploaded Leistungsbeschreibung .

---

## 1. What STEP 24 *Formally* Introduces

STEP 24 adds **hard gates** between retrieval and generation.

Before this step:

```
retrieve → always answer
```

After this step:

```
retrieve → validate → (answer | deterministic IDK)
```

This is not tuning.
This is **policy enforcement**.

---

## 2. New Canonical Rule (Non-Negotiable)

> **The LLM is never called unless retrieval quality is provably sufficient.**

This directly operationalizes the document’s core principle:

> *“KI ist ein Junior-Mitarbeiter … die letzte Instanz ist der Mensch.”* 

---

## 3. What “Thresholds” Mean (Precisely)

At STEP 24, retrieval is no longer boolean (“did we retrieve something?”) but **quantitative**.

You now expose and evaluate:

### Retrieval Signals

Typical signals (model-agnostic):

* similarity score (cosine / inner product)
* top-k score distribution
* score gap (top-1 vs top-k)
* number of chunks above minimum relevance
* document diversity (optional)

Example:

```text
Top-1 score: 0.81
Top-5 min score: 0.62
Relevant chunks ≥ threshold: 3
```

---

## 4. Threshold Enforcement Logic

You define **explicit cutoffs**.

Example (conceptual):

```python
if max_score < MIN_SCORE:
    return IDK
if num_chunks_above_threshold < MIN_CHUNKS:
    return IDK
if score_gap < MIN_GAP:
    return IDK
```

There is **no fallback**.
There is **no “try anyway.”**

This aligns exactly with the contractual disclaimer that:

* no correctness is guaranteed
* hallucinations must be avoided
* responsibility remains with humans 

---

## 5. Deterministic “I Don’t Know” (IDK)

This is the second half of STEP 24.

### Key Property

**IDK is not a model output.
IDK is a system decision.**

The LLM does *not* generate:

> “I’m not sure…”

Instead, the system returns a **fixed, audited response**.

Example:

```text
I don’t know.
The available documents do not contain sufficient information to answer this question.
```

This makes the behavior:

* reproducible
* testable
* legally defensible
* explainable to users

---

## 6. Why This Step Is Architecturally Critical

Without STEP 24:

* your RAG is probabilistic
* correctness is implicit
* failure modes are silent

With STEP 24:

* correctness is **explicit**
* uncertainty is **visible**
* failure is **safe**

This mirrors the document’s statement:

> *“Eine KI ist ein extrem schneller Musterscanner … jedoch kein denkendes Wesen.”* 

STEP 24 forces the system to **admit that limitation in code**.

---

## 7. What STEP 24 Is *Not*

Let’s be very clear:

❌ Not prompt engineering
❌ Not better embeddings
❌ Not re-ranking (though compatible)
❌ Not UX polish

✅ It is **control theory applied to RAG**

---

## 8. Contractual & Ethical Alignment (Important)

Your uploaded Leistungsbeschreibung repeatedly emphasizes:

* no liability for outcomes
* mandatory human validation
* avoidance of hallucinations
* probabilistic nature of AI outputs 

STEP 24 is the **technical enforcement** of those legal statements.

In other words:

> STEP 24 turns legal disclaimers into executable guarantees.

---

## 9. System State After STEP 24

At this point, your system can truthfully claim:

* “We only answer when documents support it.”
* “Silence is preferred over fabrication.”
* “Uncertainty is a first-class outcome.”

This is the **minimum bar** for any serious internal KI system.

---

## 10. One-Line Definition (Canonical)

> **STEP 24 introduces enforced retrieval thresholds and system-level deterministic IDK, converting RAG from a probabilistic assistant into a document-grounded, safety-bounded system.**

If you want, next we can:

* formalize threshold calibration (offline evaluation)
* design confidence reports vs IDK
* or map STEP 24 cleanly to your existing CLI / API layers
