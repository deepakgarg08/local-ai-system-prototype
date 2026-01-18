**Berlin, Germany — 18 January 2026, 16:28 CET**

Below is **STEP 18 — Retrieval Evaluation & Metrics** laid out **exactly in the same architectural style** as previous steps.
This step is **offline + test-time only** and does **NOT** touch production RAG flow.

---

# STEP 18 — Retrieval Evaluation & Metrics

## Purpose (Why STEP 18 exists)

Up to STEP 17, retrieval is *designed* well but **not measured**.

STEP 18 introduces:

* deterministic retrieval evaluation
* quantitative metrics
* regression safety for retrieval quality
* no LLM dependency

This step answers:

> *“Is retrieval actually good — and is it getting better or worse over time?”*

---

## Design Principles (Non-Negotiable)

* **No LLM calls**
* **Offline evaluation**
* **Golden queries + expected documents**
* **Pure retrieval metrics**
* **Pytest-compatible**
* **No changes to runtime RAG code**

---

## New High-Level Concepts Introduced

| Concept             | Description                                |
| ------------------- | ------------------------------------------ |
| Golden Queries      | Fixed queries with known correct documents |
| Relevance Judgments | Ground truth mapping (query → doc IDs)     |
| Metrics             | Recall@k, Precision@k, MRR                 |
| Evaluation Runner   | Script to compute metrics                  |
| Regression Tests    | Fail build if retrieval degrades           |

---

## Folder Structure to Create (STEP 18)

All STEP 18 work lives under **`evaluation/`**
This keeps **evaluation isolated** from pipelines.

```
evaluation/
├── __init__.py
│
├── datasets/
│   ├── __init__.py
│   ├── golden_queries.json
│   └── relevance_judgments.json
│
├── metrics/
│   ├── __init__.py
│   ├── precision.py
│   ├── recall.py
│   └── mrr.py
│
├── runner/
│   ├── __init__.py
│   └── run_retrieval_eval.py
│
└── reports/
    └── retrieval_metrics.json
```

---

## MKDIR Commands (Copy–Paste Ready)

Run from **project root** (`local-ai-system-prototype/`):

```bash
mkdir -p evaluation/datasets
mkdir -p evaluation/metrics
mkdir -p evaluation/runner
mkdir -p evaluation/reports

touch evaluation/__init__.py
touch evaluation/datasets/__init__.py
touch evaluation/metrics/__init__.py
touch evaluation/runner/__init__.py
```

---

## File-by-File Responsibilities

### 1️⃣ `evaluation/datasets/golden_queries.json`

**Purpose:** Fixed evaluation queries.

Example:

```json
[
  {
    "id": "Q1",
    "query": "What is the purpose of the FAISS index?"
  },
  {
    "id": "Q2",
    "query": "How does chunking work in the system?"
  }
]
```

---

### 2️⃣ `evaluation/datasets/relevance_judgments.json`

**Purpose:** Ground truth relevance mapping.

Example:

```json
{
  "Q1": ["docs/v0.1.md#faiss"],
  "Q2": ["docs/v0.1.md#chunking"]
}
```

> IDs must match chunk metadata or document identifiers.

---

### 3️⃣ `evaluation/metrics/precision.py`

**Purpose:** Precision@k

```python
def precision_at_k(retrieved: list[str], relevant: list[str], k: int) -> float:
    retrieved_k = retrieved[:k]
    if not retrieved_k:
        return 0.0
    hits = sum(1 for r in retrieved_k if r in relevant)
    return hits / len(retrieved_k)
```

---

### 4️⃣ `evaluation/metrics/recall.py`

**Purpose:** Recall@k

```python
def recall_at_k(retrieved: list[str], relevant: list[str], k: int) -> float:
    retrieved_k = retrieved[:k]
    if not relevant:
        return 0.0
    hits = sum(1 for r in retrieved_k if r in relevant)
    return hits / len(relevant)
```

---

### 5️⃣ `evaluation/metrics/mrr.py`

**Purpose:** Mean Reciprocal Rank

```python
def reciprocal_rank(retrieved: list[str], relevant: list[str]) -> float:
    for idx, r in enumerate(retrieved, start=1):
        if r in relevant:
            return 1.0 / idx
    return 0.0
```

---

### 6️⃣ `evaluation/runner/run_retrieval_eval.py`

**Purpose:** End-to-end evaluation runner.

Responsibilities:

* load golden queries
* call `retrieve_context(...)`
* compute metrics
* write report

Skeleton:

```python
import json
from pipelines.query.retriever import retrieve_context
from evaluation.metrics.precision import precision_at_k
from evaluation.metrics.recall import recall_at_k
from evaluation.metrics.mrr import reciprocal_rank

def run():
    with open("evaluation/datasets/golden_queries.json") as f:
        queries = json.load(f)

    with open("evaluation/datasets/relevance_judgments.json") as f:
        relevance = json.load(f)

    results = []

    for q in queries:
        retrieved = retrieve_context(q["query"], k=5)
        retrieved_ids = [c["id"] for c in retrieved]

        rel = relevance.get(q["id"], [])

        results.append({
            "query_id": q["id"],
            "precision@5": precision_at_k(retrieved_ids, rel, 5),
            "recall@5": recall_at_k(retrieved_ids, rel, 5),
            "mrr": reciprocal_rank(retrieved_ids, rel)
        })

    with open("evaluation/reports/retrieval_metrics.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run()
```

---

### 7️⃣ `evaluation/reports/retrieval_metrics.json`

**Purpose:** Machine-readable metric output
Used later for:

* regression checks
* CI gating (future step)

---

## What STEP 18 Enables (Critically)

| Capability                      | Status     |
| ------------------------------- | ---------- |
| Retrieval regression detection  | ✅          |
| Quantitative tuning             | ✅          |
| Threshold-based gating (future) | ✅          |
| CI enforcement                  | 🔜 STEP 19 |
| Reranker comparison             | 🔜 STEP 20 |

---

## What STEP 18 Does *NOT* Do

* ❌ No LLM scoring
* ❌ No hallucination detection
* ❌ No answer evaluation
* ❌ No production runtime impact

---

## Clean Mental Model

```
Golden Queries
      ↓
Retriever
      ↓
Retrieved Chunks
      ↓
Metrics (Recall / Precision / MRR)
      ↓
JSON Report
```

---

## Next Logical Step

**STEP 19 — Retrieval Regression Gates**

* minimum Recall@k
* fail CI if metrics drop
* protect retrieval quality permanently

If you want, I can write **STEP 18 README.md** or **pytest-based metric assertions** next.
