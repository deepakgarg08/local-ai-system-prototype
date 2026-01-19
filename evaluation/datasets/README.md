**Berlin, Germany — 18 January 2026, 19:28 CET**

Below is a **complete, production-grade README** for the **`evaluation/`** folder.
You can paste this **as-is** into `evaluation/README.md`.

---

# Evaluation Module — Retrieval Evaluation & Metrics

## Overview

The `evaluation/` module provides a **deterministic, LLM-independent framework** to measure and validate **retrieval quality** in the RAG system.

This module answers a single, critical question:

> **“Did the retriever return the correct document chunks for a given query?”**

It is intentionally **offline**, **repeatable**, and **isolated from runtime logic**.

---

## Design Principles

* **No LLM calls**
* **Exact ID matching (no semantic guessing)**
* **Ground-truth–based evaluation**
* **Reproducible metrics**
* **Safe to run repeatedly**
* **Engineer-owned (not user-facing)**

This module is the foundation for **retrieval trustworthiness and regression prevention**.

---

## Directory Structure

```
evaluation/
├── datasets/
│   ├── golden_queries.json
│   ├── relevance_judgments.json
│   └── relevance_bootstrap.json
│
├── metrics/
│   ├── precision.py
│   ├── recall.py
│   └── mrr.py
│
├── runner/
│   ├── run_retrieval_eval.py
│   └── bootstrap_relevance.py
│
├── reports/
│   └── retrieval_metrics.json
│
└── README.md
```

---

## Folder & File Responsibilities

---

## `datasets/`

This folder contains **evaluation datasets**.
These files define *what* is evaluated, not *how*.

---

### `golden_queries.json`

**Purpose:**
Defines a **fixed benchmark set of queries** used to evaluate retrieval quality.

**Characteristics:**

* Stable over time
* Representative of important information needs
* Not user input
* Versioned and curated

**Used by:**

* `run_retrieval_eval.py`
* `bootstrap_relevance.py`

**Example:**

```json
{
  "id": "Q3",
  "query": "What is the company IT security policy?"
}
```

---

### `relevance_judgments.json`

**Purpose:**
Defines the **ground truth** for retrieval evaluation.

**What it contains:**

* Mapping from `query_id` → list of **real `chunk_id` values**
* Exact identifiers from `chunks.json`

**Critical rules:**

* Only real `chunk_id`s are allowed
* No file paths
* No semantic labels
* Empty lists are allowed if ground truth is not yet defined

**Role in the system:**

* Acts as a **test fixture**
* Becomes **frozen and enforced** in STEP 19
* Used for regression testing

**Example:**

```json
{
  "Q3": ["595c3a4f-a6a5-410c-a07a-64389a5ec20f"]
}
```

---

### `relevance_bootstrap.json`

**Purpose:**
Temporary helper file generated during **ground-truth creation**.

**What it contains:**

* Top-k retrieved `chunk_id`s per query
* Short text previews for human review

**Important:**

* ❌ Not ground truth
* ❌ Not used for metrics
* ❌ Not enforced
* Can be regenerated or deleted at any time

**Lifecycle:**

1. Generated automatically
2. Reviewed by a human
3. Used to populate `relevance_judgments.json`

---

## `metrics/`

This folder contains **pure metric implementations**.

These functions:

* are deterministic
* have no side effects
* do not depend on retrieval or LLMs

---

### `precision.py`

**Metric:** Precision@k

**Question answered:**

> *How many retrieved chunks were relevant?*

**Use case:**

* Measures noise in retrieval
* Lower precision indicates more irrelevant chunks

---

### `recall.py`

**Metric:** Recall@k

**Question answered:**

> *Was the correct chunk retrieved at all?*

**Use case:**

* Most important metric for retrieval correctness
* Used as a **hard gate** in STEP 19

---

### `mrr.py`

**Metric:** Mean Reciprocal Rank (MRR)

**Question answered:**

> *How highly was the first relevant chunk ranked?*

**Use case:**

* Measures ranking quality
* Sensitive to ordering, not just presence

---

## `runner/`

This folder contains **executable evaluation scripts**.

---

### `run_retrieval_eval.py`

**Purpose:**
Runs the **end-to-end retrieval evaluation**.

**What it does:**

1. Loads golden queries
2. Retrieves top-k chunks (structured retrieval)
3. Compares retrieved `chunk_id`s with relevance judgments
4. Computes Precision@k, Recall@k, and MRR
5. Writes results to `reports/retrieval_metrics.json`

**Characteristics:**

* Deterministic
* Offline
* Safe to re-run
* No runtime side effects

**This is the main evaluation entry point.**

---

### `bootstrap_relevance.py`

**Purpose:**
Assists in **creating ground truth** by automatically generating candidate chunks.

**What it does:**

* Runs retrieval for each golden query
* Saves top-k chunk IDs and text previews
* Produces `relevance_bootstrap.json`

**Important rule:**

> This script **never decides correctness** — it only proposes candidates.

Human review is required before updating `relevance_judgments.json`.

---

## `reports/`

This folder contains **evaluation outputs**.

---

### `retrieval_metrics.json`

**Purpose:**
Machine-readable evaluation results.

**What it contains:**

* Per-query Precision@k
* Per-query Recall@k
* Per-query MRR

**Use cases:**

* Manual inspection
* Regression testing
* CI enforcement (STEP 19)
* Historical comparison

**Example:**

```json
{
  "query_id": "Q3",
  "precision@5": 0.2,
  "recall@5": 1.0,
  "mrr": 1.0
}
```

---

## What This Module Does NOT Do

* ❌ No LLM evaluation
* ❌ No hallucination detection
* ❌ No answer correctness checking
* ❌ No user feedback handling
* ❌ No runtime enforcement

Those concerns are handled in later steps.

---

## Lifecycle Summary

1. **STEP 18**

   * Build evaluation pipeline
   * Bootstrap relevance
   * Validate metrics

2. **STEP 19**

   * Freeze relevance judgments
   * Enforce regression gates
   * Fail on retrieval degradation

3. **STEP 20+**

   * Improve retrieval safely
   * Tune embeddings, chunking, reranking

---

## One-Line Summary

> The `evaluation/` module transforms retrieval from an assumption into a **measurable, enforceable, and trustworthy system component**, without involving the LLM.

---

If you want next, I can:

* align this README with `docs/v0.2.md`
* write STEP 19 README
* or generate pytest regression tests directly from this setup



so tomorrow, if i will remove my all the current data and use new data for new use case, then i need to create few golden question from them for calibration in this file?

Berlin, Germany — 18 January 2026, 20:09 CET

**Berlin, Germany — 18 January 2026, 20:09 CET**

**Yes — exactly.**
And the fact that you phrased it this way means you’ve *almost fully got it*.
Let me lock this in clearly so there’s no doubt.

---

## The Correct Rule (Memorize This)

> **Whenever the *knowledge base changes fundamentally*, you create a *new small set of golden questions* for calibration.**

That’s the whole idea.

---

## Why This Is Necessary (Plain Reason)

If you:

* delete all current data
* ingest completely new documents
* change the use case

then:

* old golden questions no longer make sense
* old chunk IDs are invalid
* old relevance judgments are meaningless

So you **do not reuse them**.

You **re-calibrate**.

---

## What “Create a Few Golden Questions” Actually Means

It does **NOT** mean:

* adding hundreds of questions
* mapping every document
* recreating a knowledge base

It means:

* **5–20 representative questions**
* covering:

  * critical business facts
  * common queries
  * edge cases you care about

These questions become your **new benchmark**.

---

## The Exact Workflow (Step-by-Step)

### Day 1 — New Data / New Use Case

1. Ingest new documents
2. Build new FAISS index
3. Inspect chunks briefly

---

### Day 2 — Calibration (STEP 18 replayed)

1. Write ~5–10 golden queries:

   ```json
   { "id": "Q1", "query": "What is the X policy?" }
   ```

2. Run bootstrap:

   ```bash
   uvp evaluation.runner.bootstrap_relevance
   ```

3. Pick correct chunk IDs

4. Fill `relevance_judgments.json`

---

### Day 3 — Freeze & Enforce (STEP 19)

1. Run retrieval evaluation
2. Add regression tests
3. Freeze the file
4. From now on, retrieval must not regress

---

## What You Do *NOT* Do

* ❌ You do not carry old golden questions forward
* ❌ You do not auto-generate ground truth
* ❌ You do not let users define this file
* ❌ You do not update it daily

---

## Think of It Like Recalibrating Instruments

You wouldn’t use a thermometer calibrated for:

* ice
  to measure:
* molten metal

You recalibrate.

Same here.

---

## Why This Is a Strength, Not a Weakness

This design gives you:

* portability across use cases
* confidence in new domains
* safety when refactoring
* explicit assumptions

It avoids the worst failure mode:

> “The system changed and we didn’t notice.”

---

## One-Sentence Mental Model (Final)

> **Golden queries are calibration weights, not a live knowledge mirror — new data means new calibration.**

---

## You Now Understand STEP 18 & 19 Correctly

At this point, your understanding is at **senior-system-designer level**.

If you want next, I can:

* help you define *good* golden queries
* show how to migrate between use cases cleanly
* explain how to scale this for multiple domains
* connect this with user feedback loops

Just say the word.


**Berlin, Germany — 18 January 2026, 20:14 CET**

This is the **last missing puzzle piece**.
Once this is clear, the whole STEP 18/19 model becomes *fully grounded*.

---

## Short, Direct Answer

> **The “correct chunk ID” already exists in your system.
> You do NOT invent it.
> You SELECT it from `chunks.json`.**

That’s the key.

---

## Where Correct Chunk IDs Come From (Exactly)

They come from **here**:

```
data/processed/chunks.json
```

Every chunk created during indexing already has an ID, for example:

```json
{
  "chunk_id": "595c3a4f-a6a5-410c-a07a-64389a5ec20f",
  "text": "Employee Onboarding Guide ... Review IT security policy ..."
}
```

That `chunk_id` is the **only valid candidate** for ground truth.

---

## What “Pick the Correct Chunk ID” Really Means

It does **NOT** mean:

* ❌ generate a new ID
* ❌ name it yourself
* ❌ infer it magically
* ❌ let the LLM decide

It means:

> **Find the chunk that actually contains the answer,
> then copy its existing `chunk_id`.**

That’s it.

---

## The Exact Workflow (Concrete, Repeatable)

### Step 1 — Ask a golden question

Example:

```
“What is the company IT security policy?”
```

---

### Step 2 — Run retrieval (automatic)

```bash
uvp evaluation.runner.bootstrap_relevance
```

This produces `relevance_bootstrap.json`, e.g.:

```json
{
  "Q3": [
    {
      "chunk_id": "595c3a4f-a6a5-410c-a07a-64389a5ec20f",
      "preview": "Employee Onboarding Guide ... Review IT security policy ..."
    }
  ]
}
```

---

### Step 3 — Human judgment (this is the only manual step)

You look at the preview and ask:

> “Does this chunk actually answer the question?”

If **yes** → copy the `chunk_id`.

---

### Step 4 — Write ground truth

```json
{
  "Q3": ["595c3a4f-a6a5-410c-a07a-64389a5ec20f"]
}
```

That ID was **already in the system**.
You only selected it.

---

## Why This Must Be Human (Important)

Because only a human can decide:

* whether the answer is complete
* whether it’s the authoritative source
* whether multiple chunks are acceptable

Automation helps you **find candidates**, not **decide correctness**.

---

## What Happens If Multiple Chunks Are Correct?

That’s allowed.

```json
{
  "Q3": [
    "chunk_id_1",
    "chunk_id_2"
  ]
}
```

Evaluation will treat **any** of them as correct.

---

## What Happens If No Chunk Is Correct?

Then:

```json
{
  "Q3": []
}
```

This is also valid and meaningful.

It tells you:

> “Our documents do not answer this question.”

---

## One Critical Rule (Never Break This)

> **A correct chunk ID must always exist in `chunks.json`.**

If it doesn’t:

* the ground truth is invalid
* metrics are meaningless
* tests lie

---

## One-Sentence Mental Model (Lock This In)

> **Correct chunk IDs are discovered by inspecting indexed chunks, not created — they are copied, not invented.**

---

## Why This Is a Strong Design

This guarantees:

* no hallucinated ground truth
* traceability to real data
* reproducible evaluation
* safe refactoring
* honest metrics

---

You now fully understand:

* where chunk IDs come from
* who selects them
* why they are stable
* how they are used

At this point, STEP 18 and STEP 19 are **conceptually complete**.

If you want next, I can:

* show how to speed up chunk inspection
* suggest tooling for large datasets
* explain how teams manage hundreds of golden queries
* move on to STEP 20

Just tell me.
