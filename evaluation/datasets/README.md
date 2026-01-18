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
