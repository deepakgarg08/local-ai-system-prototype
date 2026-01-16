from pathlib import Path
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# Project-root–anchored paths (CORRECT WAY)
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
print(f"Project root: {PROJECT_ROOT}")

DATA_DIR = PROJECT_ROOT / "data"
INDEX_DIR = DATA_DIR / "indexes"

FAISS_INDEX_PATH = INDEX_DIR / "faiss.index"
METADATA_PATH = INDEX_DIR / "metadata.json"

# --------------------------------------------------
# Embedding model (MUST match indexing)
# --------------------------------------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL)


def load_faiss():
    index = faiss.read_index(str(FAISS_INDEX_PATH))

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata

# STEP 9B — Embed the User Query
def embed_query(query: str) -> np.ndarray:
    vec = model.encode(
        [query],
        normalize_embeddings=True
    )
    return vec.astype("float32")


def search(query: str, top_k: int = 5):
    index, metadata = load_faiss()
    query_vec = embed_query(query)

    distances, indices = index.search(query_vec, top_k)
    
    # print("type(metadata), len(metadata)", type(metadata), len(metadata))
    print("metadata[0].keys()", metadata[0].keys())

    results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        item = metadata[idx]   # ← FIXED HERE

        results.append({
            "score": float(score),
            "text": item["text"],
            "source": item.get("source"),
            "chunk_id": idx
        })
        


    return results


# --------------------------------------------------
# Example usage
# --------------------------------------------------

if __name__ == "__main__":
    query = input("Enter your query: ").strip()

    hits = search(query, top_k=5)

    print("\nTop results:\n")
    for i, h in enumerate(hits, 1):
        print(f"[{i}] Score: {h['score']:.4f}")
        print(f"Source: {h['source']}")
        print(h["text"])
        print("-" * 80)
