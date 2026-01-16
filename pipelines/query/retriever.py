"""
FAISS-based retrieval layer (disk-backed)
"""

from pathlib import Path
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Base project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Paths
INDEX_DIR = BASE_DIR / "data" / "indexes"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

FAISS_INDEX_PATH = INDEX_DIR / "faiss.index"
CHUNKS_PATH = PROCESSED_DIR / "chunks.json"

# Load embedding model (MUST match indexing step)
_embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS index
_index = faiss.read_index(str(FAISS_INDEX_PATH))

# Load chunk metadata
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    _chunks = json.load(f)


def retrieve_context(query: str, k: int = 4) -> list[str]:
    """
    Retrieve top-k relevant text chunks for a query.
    """
    query_embedding = _embedding_model.encode(
        [query],
        normalize_embeddings=True,
    )

    distances, indices = _index.search(
        np.array(query_embedding, dtype="float32"),
        k,
    )

    results = []
    for idx in indices[0]:
        if idx == -1:
            continue
        results.append(_chunks[idx]["text"])

    return results
