import faiss
import json
import numpy as np
from pipelines.embeddings.embedder import Embedder

INDEX_PATH = "data/indexes/faiss.index"
META_PATH = "data/indexes/metadata.json"

_embedder = Embedder()


def vector_search(query: str, top_k: int = 10):
    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH) as f:
        metadata = json.load(f)

    query_vec = _embedder.embed([query])
    query_vec = np.array(query_vec).astype("float32")

    scores, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = metadata[idx]
        chunk["score"] = float(score)
        results.append(chunk)

    return results
