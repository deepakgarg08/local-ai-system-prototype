
**📅 19 January 2026, 14:07 CET (Berlin, Germany)**

---

# 👉 STEP 20.3 — Cross-Encoder Reranking

This step **upgrades retrieval quality** by inserting a **cross-encoder reranking stage** *after* vector retrieval and *before* prompt assembly.

At this point in the project:

* You already have **FAISS-based bi-encoder retrieval**
* You already enforce **grounding & gating**
* What’s missing is **fine-grained relevance ordering**

Cross-encoders solve exactly that.

---

## 1️⃣ Why Cross-Encoder Reranking Exists (Concept First)

### Problem with pure vector search (bi-encoder)

FAISS + embeddings:

* Encode **query** and **documents separately**
* Fast ✅
* Approximate ❌ (semantic but shallow)

This often leads to:

* Correct topic, wrong sentence
* High recall, imperfect precision

### What a Cross-Encoder Does

A **cross-encoder**:

* Takes `(query, chunk)` **together**
* Runs a transformer over the pair
* Outputs a **true relevance score**

This gives:

* Slower ❌ (but applied only to top-k)
* Much higher precision ✅

### Canonical pipeline after this step

```
Query
 └─ FAISS (bi-encoder, fast) → top_k=20
      └─ Cross-Encoder rerank → top_n=5
           └─ Prompt Assembly
                └─ LLM
```

---

## 2️⃣ New Folder Structure (STEP 20.3)

We keep **strict separation of concerns**.

```
pipelines/
└── reranking/
    ├── __init__.py
    ├── base.py
    ├── cross_encoder.py
    └── rerank.py
```

### Why a new `reranking/` pipeline?

Because:

* Reranking is **not retrieval**
* Reranking is **not prompting**
* It is an **independent decision layer**

This keeps the architecture clean and testable.

---

## 3️⃣ Folder & File Creation (Commands)

```bash
mkdir -p pipelines/reranking
touch pipelines/reranking/__init__.py
touch pipelines/reranking/base.py
touch pipelines/reranking/cross_encoder.py
touch pipelines/reranking/rerank.py
```

---

## 4️⃣ `base.py` — Reranker Contract

### Why this file exists

* Enforces **pluggability**
* Allows future rerankers (LLM-based, heuristic, hybrid)

### `pipelines/reranking/base.py`

```python
from abc import ABC, abstractmethod
from typing import List, Dict


class BaseReranker(ABC):
    @abstractmethod
    def rerank(
        self,
        query: str,
        chunks: List[Dict],
        top_n: int,
    ) -> List[Dict]:
        """
        Rerank retrieved chunks by relevance.

        Each chunk must contain:
        - text
        - metadata
        - score (optional, from retriever)
        """
        raise NotImplementedError
```

---

## 5️⃣ `cross_encoder.py` — Concrete Implementation

### Why this file exists

* Implements **true semantic relevance**
* Isolates ML dependency (sentence-transformers)

### Model choice (default)

A common, strong baseline:

```
cross-encoder/ms-marco-MiniLM-L-6-v2
```

### `pipelines/reranking/cross_encoder.py`

```python
from typing import List, Dict
from sentence_transformers import CrossEncoder

from pipelines.reranking.base import BaseReranker


class CrossEncoderReranker(BaseReranker):
    def __init__(self, model_name: str):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        chunks: List[Dict],
        top_n: int,
    ) -> List[Dict]:
        if not chunks:
            return []

        pairs = [(query, chunk["text"]) for chunk in chunks]
        scores = self.model.predict(pairs)

        for chunk, score in zip(chunks, scores):
            chunk["rerank_score"] = float(score)

        reranked = sorted(
            chunks,
            key=lambda c: c["rerank_score"],
            reverse=True,
        )

        return reranked[:top_n]
```

---

## 6️⃣ `rerank.py` — Orchestration Function

### Why this file exists

* Mirrors your existing design:

  * `retrieve_context`
  * `run_rag`
* Keeps **policy decisions** out of the model class

### `pipelines/reranking/rerank.py`

```python
from typing import List, Dict

from pipelines.reranking.cross_encoder import CrossEncoderReranker


def rerank_chunks(
    query: str,
    chunks: List[Dict],
    top_n: int,
) -> List[Dict]:
    reranker = CrossEncoderReranker(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    return reranker.rerank(
        query=query,
        chunks=chunks,
        top_n=top_n,
    )
```

---

## 7️⃣ Integration Point (Where It Is Used)

### Before STEP 20.3

```
retrieve_context → prompt → LLM
```

### After STEP 20.3

```
retrieve_context
   → rerank_chunks
        → prompt
             → LLM
```

This will typically be wired inside:

```
pipelines/query/run_rag.py
```

---

## 8️⃣ Test Cases (Required ✅)

### Why tests are required here

* Cross-encoders are **deterministic**
* Sorting errors are catastrophic but silent
* Easy to test without LLMs

---

### Test folder

```bash
mkdir -p tests/reranking
touch tests/reranking/test_cross_encoder_reranker.py
```

---

### `test_cross_encoder_reranker.py`

```python
from pipelines.reranking.cross_encoder import CrossEncoderReranker


def test_reranker_orders_chunks_by_score():
    reranker = CrossEncoderReranker(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    query = "What is machine learning?"

    chunks = [
        {"text": "Bananas are yellow.", "metadata": {}},
        {"text": "Machine learning is a field of AI.", "metadata": {}},
    ]

    reranked = reranker.rerank(
        query=query,
        chunks=chunks,
        top_n=1,
    )

    assert len(reranked) == 1
    assert "machine learning" in reranked[0]["text"].lower()
```

---

## 9️⃣ What STEP 20.3 Achieves Architecturally

| Layer                 | Status            |
| --------------------- | ----------------- |
| Retrieval             | Fast, high recall |
| **Reranking**         | ✅ High precision  |
| Grounding             | Enforced          |
| Hallucination control | Strong            |
| Explainability        | Improved (scores) |

You have now **separated concerns cleanly**:

* FAISS = candidate generation
* Cross-encoder = judgment
* LLM = synthesis only

---

## 🔜 Next Logical Steps

**STEP 20.4 — Score-Aware Prompt Assembly**

* Pass rerank scores into the prompt
* Weight citations
* Improve confidence explanations

If you want, I can continue directly with **STEP 20.4** or show how to **benchmark before/after reranking**.
