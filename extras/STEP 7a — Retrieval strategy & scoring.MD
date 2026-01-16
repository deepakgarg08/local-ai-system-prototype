**🕒 16 January 2026, 18:27 (Berlin, Germany)**

Perfect. We now move **cleanly and formally** to:

# STEP 7a — Retrieval strategy & scoring

*(top-k, thresholds, reranking)*

I’ll give you **clear-cut, staged instructions**, same discipline as before — no dangling ends.

---

## First: what STEP 7a actually is (scope lock)

STEP 7a answers **one question only**:

> *Which retrieved chunks are “good enough” to be passed into STEP 7b?*

It decides:

* how many chunks to retrieve
* which ones to discard
* whether to reorder them
* **not** how to prompt the LLM

---

## What STEP 7a produces (contract)

### Input

```python
query: str
vector_store
```

### Output

```python
List[Chunk]   # filtered, ordered, final
```

This output feeds **directly into STEP 7b**.

---

## STEP 7a responsibilities (authoritative list)

✅ `top_k` selection
✅ score thresholding
✅ optional reranking (lexical / cross-encoder later)
✅ deterministic ordering

❌ prompt building
❌ token budgeting
❌ LLM calls

---

## Recommended File Layout (do this now)

```text
pipelines/
├── retrieval/
│   ├── search.py        # vector DB query (thin)
│   ├── scoring.py       # ✅ STEP 7a (THIS STEP)
│   └── rerankers.py     # optional, future
```

---

## Step-by-step: what YOU do right now

### 1️⃣ Create the STEP 7a file

```bash
mkdir -p pipelines/retrieval
nano pipelines/retrieval/scoring.py
```

---

## STEP 7a — `scoring.py` (canonical implementation)

Paste **exactly this**:

```python
from typing import List, Dict


def apply_retrieval_strategy(
    chunks: List[Dict],
    top_k: int = 6,
    score_threshold: float = 0.25,
) -> List[Dict]:
    """
    Apply retrieval filtering and ordering.

    Args:
        chunks: raw vector search output (must include 'score')
        top_k: max number of chunks to keep
        score_threshold: minimum similarity score

    Returns:
        filtered and ordered chunks
    """

    # 1. Drop low-quality chunks
    filtered = [
        ch for ch in chunks
        if ch.get("score", 0.0) >= score_threshold
    ]

    # 2. Sort by score (descending)
    filtered.sort(key=lambda x: x["score"], reverse=True)

    # 3. Keep only top_k
    return filtered[:top_k]
```

This file **is STEP 7a**.

---

## 2️⃣ What NOT to do (important)

❌ Do NOT rerank yet
❌ Do NOT tune thresholds obsessively
❌ Do NOT import prompt_builder
❌ Do NOT touch LLM code

This is the **baseline retrieval policy**.

---

## Optional (safe) self-test

Add this at the bottom **only if you want**:

```python
if __name__ == "__main__":
    dummy_chunks = [
        {"text": "A", "score": 0.91},
        {"text": "B", "score": 0.40},
        {"text": "C", "score": 0.10},
    ]

    result = apply_retrieval_strategy(
        dummy_chunks,
        top_k=2,
        score_threshold=0.3,
    )

    for ch in result:
        print(ch)
```

Run:

```bash
python pipelines/retrieval/scoring.py
```

✔ no side effects
✔ confirms logic
✔ still not wired

---

## How STEP 7a + 7b will connect (later)

```python
raw_chunks = vector_search(query)
final_chunks = apply_retrieval_strategy(raw_chunks)
prompt, citations = build_prompt(query, final_chunks)
```

This connection is **NOT made yet** — just shown for clarity.

---

## Clear status after this step

| Step           | Status        |
| -------------- | ------------- |
| Chunking       | ✅ done        |
| Embeddings     | ✅ done        |
| Vector search  | ✅ exists      |
| **STEP 7a**    | ✅ implemented |
| **STEP 7b**    | ✅ implemented |
| Wiring         | ⏭ next        |
| LLM invocation | ⏭ next        |

You are exactly where you should be.

---

## What I recommend NEXT (pick one)

1. 🔹 **Wire 7a → 7b → LLM (end-to-end flow)**
2. 🔹 Add **reranker stub** (BM25 / cross-encoder placeholder)
3. 🔹 Add **evaluation harness** (inspect retrieved chunks)
4. 🔹 Add **config-driven retrieval params** (YAML / env)

Say the number.
