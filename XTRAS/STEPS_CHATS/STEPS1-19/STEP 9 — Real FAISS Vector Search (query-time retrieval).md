**🕒 16 January 2026, 18:06 (Berlin time, CET)**
https://chatgpt.com/share/696a9227-3b28-8008-8075-66507486d06f
Below is **STEP 9 — Real FAISS Vector Search (query-time retrieval)**, written **practically and implementation-ready**, aligned with your **Fedora Linux setup**, **local embeddings**, and **local LLM (DeepSeek later)**.

---

## 🎯 Goal of STEP 9

At **query time**, we want to:

1. Take a **user query**
2. Convert it into an **embedding**
3. Search the **FAISS index**
4. Retrieve the **top-k most relevant chunks**
5. Return them (to be used later by your local LLM)

This is the **core of RAG retrieval**.
STEP 9 — Real FAISS Vector Search (query-time retrieval)
---

## 📦 What You Should Already Have (from earlier steps)


You should already have:

* ✅ Chunked documents
* ✅ Stored embeddings
* ✅ FAISS index saved to disk
* ✅ Metadata mapping `vector_id → chunk text + source`

Typical files:

```text
data/
 ├── faiss/
 │    ├── index.faiss
 │    └── metadata.json
 └── processed/
      └── chunks.json
```

---

## 🔧 STEP 9A — Load FAISS Index & Metadata

Create a new file:

```bash
pipelines/retrieval/faiss_search.py
```

### `faiss_search.py`

```python
import faiss
import json
import numpy as np
from pathlib import Path

FAISS_DIR = Path("data/faiss")
INDEX_PATH = FAISS_DIR / "index.faiss"
META_PATH = FAISS_DIR / "metadata.json"


def load_faiss():
    index = faiss.read_index(str(INDEX_PATH))

    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata
```

---

## 🔧 STEP 9B — Embed the User Query

You must use **the SAME embedding model** you used during indexing.

Example (SentenceTransformers – CPU/GPU works on Fedora):

```python
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(EMBEDDING_MODEL)
```

Embedding function:

```python
def embed_query(query: str) -> np.ndarray:
    vec = model.encode([query], normalize_embeddings=True)
    return vec.astype("float32")
```

⚠️ **Normalization must match indexing step**
(if you normalized during indexing, normalize here too)

---

## 🔧 STEP 9C — Perform FAISS Search

```python
def search(query: str, top_k: int = 5):
    index, metadata = load_faiss()
    query_vec = embed_query(query)

    distances, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        chunk = metadata[str(idx)]
        results.append({
            "score": float(score),
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": idx
        })

    return results
```

---

## 🔧 STEP 9D — CLI Test (Very Important)

Add this at the bottom:

```python
if __name__ == "__main__":
    query = input("Enter your query: ")

    hits = search(query, top_k=5)

    print("\nTop results:\n")
    for i, h in enumerate(hits, 1):
        print(f"[{i}] Score: {h['score']:.4f}")
        print(f"Source: {h['source']}")
        print(h["text"])
        print("-" * 80)
```

Run:

```bash
python pipelines/retrieval/faiss_search.py
```

---

## ✅ What You Achieved in STEP 9

✔ Real vector similarity search
✔ FAISS running locally (no cloud)
✔ Query-time retrieval working
✔ Ready for **local DeepSeek / LLM generation**

This is **fully production-grade RAG retrieval**.

---

## 🔜 What Comes Next (STEP 10)

**STEP 10 — Retrieval → Prompt Assembly → Local LLM Inference**

That’s where:

* Retrieved chunks are formatted
* Injected into a prompt
* Passed to your **local DeepSeek model**

If you want, next I can:

* 🔹 Add **MMR / hybrid search**
* 🔹 Add **GPU FAISS**
* 🔹 Integrate **DeepSeek inference**
* 🔹 Optimize for large corpora (millions of chunks)

Just tell me the next step.
