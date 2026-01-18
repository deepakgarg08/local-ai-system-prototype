"""
FAISS-based retrieval layer (disk-backed)
"""

from pathlib import Path
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

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


def retrieve_context(query: str, k: int = 4) -> List[str]:
    """
    Backward-compatible retrieval.
    Returns ONLY text chunks.
    """
    scored = retrieve_context_with_scores(query, k)
    return [text for text, _ in scored]


def retrieve_context_with_scores(
    query: str,
    k: int = 4
) -> List[Tuple[str, float]]:
    """
    Retrieve top-k chunks WITH similarity scores.

    Returns:
        [
            (chunk_text, similarity_score),
            ...
        ]

    similarity_score ∈ [-1, 1]
    (cosine similarity)
    """

    # Embed query (same normalization as indexing)
    query_embedding = _embedding_model.encode(
        [query],
        normalize_embeddings=True,
    )

    distances, indices = _index.search(
        np.array(query_embedding, dtype="float32"),
        k,
    )

    results: List[Tuple[str, float]] = []

    for idx, distance in zip(indices[0], distances[0]):
        if idx == -1:
            continue

        # For normalized vectors:
        # cosine_similarity = 1 - distance
        similarity = 1.0 - float(distance)

        chunk_text = _chunks[idx]["text"]
        results.append((chunk_text, similarity))

    return results
