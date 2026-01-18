**Berlin, Germany — 18 January 2026, 14:18 CET**

---

# STEP 17 — Retrieval Quality Optimization (v0.3)

This step **tightens the trust boundary** of your RAG system.
While STEP 14–16 established *grounding, gating, and confidence explainability*, STEP 17 focuses on **retrieval signal quality** and **answer eligibility discipline**.

The guiding principle:

> **Bad retrieval must fail early, loudly, and deterministically — before the LLM speaks.**

---

## What STEP 17 Solves (Precisely)

| Problem                 | Status before     | Status after                 |
| ----------------------- | ----------------- | ---------------------------- |
| Similarity scores exist | Yes               | Yes                          |
| Similarity meaning      | Implicit          | **Explicit & calibrated**    |
| Noise chunks            | Returned          | **Suppressed**               |
| Weak context answers    | Sometimes allowed | **Blocked**                  |
| Confidence inflation    | Possible          | **Downgraded automatically** |
| LLM overreach           | Guarded           | **Strictly constrained**     |

---

## Focus Areas (Mapped to Concrete Mechanisms)

---

## 1️⃣ Similarity Threshold Tuning

### Goal

Convert raw FAISS distances into **semantic relevance decisions**.

### Key Insight

Similarity is **not binary** — it must be *interpreted in bands*.

### Introduced Concepts

```text
HIGH_RELEVANCE
MEDIUM_RELEVANCE
LOW_RELEVANCE
NO_RELEVANCE
```

### Example Thresholds (configurable)

```python
SIMILARITY_THRESHOLDS = {
    "high": 0.78,
    "medium": 0.62,
    "low": 0.50
}
```

### Enforcement

* Retrieval returns **(chunk, score)**
* Scores are **normalized**
* Each chunk is classified into a relevance band

> Below `low` → chunk is discarded immediately

---

## 2️⃣ Noise Chunk Suppression

### Problem

FAISS *always* returns top-k, even if all matches are garbage.

### Solution

A **two-stage filter**:

#### Stage A — Score Gate

```text
score < low_threshold → DROP
```

#### Stage B — Semantic Sanity Checks

Applied **after score filtering**:

* Chunk length too small
* Excessive boilerplate
* Metadata mismatch (wrong document type / version)
* Duplicate semantic content

### Result

Only **signal-bearing chunks** survive.

---

## 3️⃣ Confidence Downgrade Rules

### Goal

Confidence must reflect **retrieval strength**, not LLM fluency.

### Deterministic Rules

| Retrieval Outcome  | Confidence |
| ------------------ | ---------- |
| ≥1 HIGH chunk      | HIGH       |
| Only MEDIUM chunks | MEDIUM     |
| Only LOW chunks    | LOW        |
| No eligible chunks | NONE       |

### Important

Confidence is computed **before** LLM invocation.

LLM **cannot raise confidence**.

---

## 4️⃣ Stricter Answer Eligibility

### Hard Rule (New)

> **No eligible chunks → No LLM call**

### Eligibility Conditions

The answer pipeline proceeds **only if**:

* At least one chunk ≥ `medium`
* Total token budget ≥ minimum context size
* Chunk sources are traceable

Otherwise:

```text
"I don't know.
The available documents do not contain sufficient information."
```

This response is **not a failure** — it is a **correct system behavior**.

---

## STEP 17 — New & Updated Folder Structure

Below is the **complete canonical structure** after STEP 17.

```
local-ai-system-prototype/
│
├── docs/
│   ├── v0.1.md
│   ├── v0.2.md
│   ├── v0.3.md                ← STEP 17 documented here
│
├── data/
│   ├── raw/
│   ├── processed/
│   │   ├── chunks.json
│   │   └── chunk_stats.json   ← NEW: length, entropy, source stats
│   └── indexes/
│       └── faiss.index
│
├── configs/
│   ├── __init__.py
│   ├── runtime.py
│   └── retrieval.py           ← NEW: thresholds & tuning knobs
│
├── llms/
│   ├── base.py
│   ├── ollama.py
│   ├── openai.py
│   └── registry.py
│
├── pipelines/
│   ├── indexing/
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   └── build_index.py
│   │
│   ├── prompting/
│   │   └── assemble_prompt.py
│   │
│   └── query/
│       ├── retriever.py        ← UPDATED: returns scores + metadata
│       ├── relevance.py        ← NEW: threshold classification
│       ├── noise_filter.py     ← NEW: chunk suppression logic
│       ├── eligibility.py     ← NEW: answer gating rules
│       ├── confidence.py      ← UPDATED: downgrade logic
│       └── run_rag.py          ← UPDATED: strict orchestration
│
├── evaluation/
│   ├── retrieval_diagnostics.py  ← NEW: score distribution analysis
│   └── false_positive_audit.py   ← NEW: noise inspection
│
├── tests/
│   ├── test_relevance.py
│   ├── test_noise_filter.py
│   ├── test_eligibility.py
│   └── test_confidence.py
│
├── .env
├── pyproject.toml
└── README.md
```

---

## Updated Query-Time Flow (STEP 17)

```
query
  ↓
FAISS retrieve (k)
  ↓
score normalization
  ↓
relevance classification
  ↓
noise suppression
  ↓
eligibility check
  ├── FAIL → deterministic "I don't know"
  └── PASS
        ↓
prompt assembly
        ↓
LLM
        ↓
confidence assignment
        ↓
answer + sources
```

---

## Why STEP 17 Is a Critical Maturity Step

After this step, your system is no longer:

> “RAG that usually behaves”

It becomes:

> **A retrieval-governed system where the LLM is a controlled renderer, not a knowledge source**

This aligns **perfectly** with:

* your STEP 15 confidence explainability
* your STEP 16 operational discipline
* and the philosophical constraints outlined in your project documents

---

## Next Logical Step (STEP 18 — Optional Preview)

If you want to proceed next, the natural evolution is:

**STEP 18 — Retrieval Evaluation & Metrics**

* golden queries
* recall@k / precision@k
* false-positive tracking
* threshold auto-tuning (offline)

---

If you want:

* concrete threshold values for your embedding model
* example implementations for `noise_filter.py`
* or pytest-ready test cases

tell me **which part to drill into first**.


**Berlin, Germany — 18 January 2026, 15:36 CET**

---

# STEP 17 — Retrieval Quality Optimization (Summary)

## Objective

STEP 17 strengthens the **trustworthiness of the RAG system** by improving retrieval quality handling and reducing hallucination risk, especially in scenarios with:

* small internal datasets
* limited or sparse context
* smaller / weaker LLMs

The step introduces **retrieval-aware control over when and how the LLM is allowed to answer**, without changing the core architecture.

---

## Core Problems Addressed

Before STEP 17:

* Retrieval could be *technically relevant* but *semantically weak*
* Small corpora were penalized by rigid thresholds
* Small models tended to “fill gaps” even when context was thin
* Prompting did not adapt to evidence strength

STEP 17 explicitly fixes these issues.

---

## Key Design Principles Introduced

1. **Evidence strength matters more than evidence volume**
2. **Small corpora require adaptive rules, not relaxed safety**
3. **The LLM is a renderer of evidence, not a knowledge source**
4. **Hallucination prevention is a system concern, not a model hope**

---

## Main Changes in STEP 17

### 1. Retrieval Quality Awareness

* Retrieval results are no longer treated uniformly
* The system reasons about:

  * number of retrieved chunks
  * total context size (tokens)
  * corpus maturity (`small`, `growing`, `mature`)
* These signals influence downstream behavior

No changes were made to:

* FAISS
* embeddings
* retrieval mechanics

---

### 2. Corpus-Aware Behavior (`CORPUS_PROFILE`)

A new configuration flag was introduced:

```python
CORPUS_PROFILE = "small"
```

Purpose:

* Explicitly model dataset maturity
* Avoid over-strict blocking for small datasets
* Allow stricter behavior later without refactoring

This flag is:

* defined in configuration
* consumed only by query orchestration
* never inferred automatically

---

### 3. Extractive-Only Answer Mode (Critical)

STEP 17 introduces **extractive-only prompting** to contain hallucinations.

When activated:

* The LLM is forced to:

  * quote or closely paraphrase context
  * avoid explanations or generalizations
  * reuse context terminology
* If information is missing, the model must say *“I don’t know”*

This mode is triggered when:

* corpus is small **and**
* context is minimal (e.g. single chunk or very few tokens)

---

### 4. Prompting Layer Hardening

Changes were applied in the **prompt assembly layer**, not retrieval:

* Instructions were centralized
* Strong, explicit grounding rules were enforced
* Extractive constraints are injected conditionally

This ensures:

* consistent behavior across models
* better compliance from smaller LLMs
* no reliance on model “judgment”

---

### 5. Orchestration-Level Control

The query orchestrator (`run_rag`) now:

* decides *when* extractive-only mode is required
* passes this decision explicitly to the prompt layer
* keeps the LLM blind to:

  * similarity scores
  * confidence
  * corpus size

This preserves clean separation of concerns.

---

## What STEP 17 Does **Not** Do

* ❌ No retraining
* ❌ No embedding changes
* ❌ No FAISS tuning
* ❌ No confidence inflation
* ❌ No relaxation of grounding rules

Safety guarantees from earlier steps remain intact.

---

## Resulting System Behavior

After STEP 17, the system:

* answers more often **when evidence is strong but small**
* refuses confidently **when evidence is weak**
* hallucinates significantly less with small models
* remains usable during early data accumulation
* scales naturally as the corpus grows

---

## Position in the Overall Roadmap

STEP 17 transitions the system from:

> *“Grounded RAG”*

to:

> **“Retrieval-governed, hallucination-aware RAG”**

It is a **stability and trust milestone**, not a feature expansion.

---

## One-Line Takeaway

> **STEP 17 ensures that the system adapts its answering behavior to the quality and maturity of retrieved evidence, not to the confidence of the LLM.**

---

If you want, the next natural step would be:

**STEP 18 — Retrieval Evaluation & Metrics**
(measuring false positives, recall, and threshold quality offline)

Just tell me when you’re ready.
