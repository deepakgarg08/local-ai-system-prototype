"""
FAISS-based retrieval layer (disk-backed)
"""

from pathlib import Path
import json
import faiss
import numpy as np
from typing import List, Tuple
from pipelines.confidence.scorer import score_confidence
from typing import List, Dict
from pipelines.embeddings.embedder import Embedder
# Base project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Paths
INDEX_DIR = BASE_DIR / "data" / "indexes"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

FAISS_INDEX_PATH = INDEX_DIR / "faiss.index"
CHUNKS_PATH = PROCESSED_DIR / "chunks.json"

_embedder = Embedder()

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
    return [item["text"] for item in scored]


def retrieve_context_with_scores(
    query: str,
    k: int = 4,
    allowed_document_ids: list[str] | None = None
    ):

    """
    Retrieve top-k chunks WITH similarity scores.

    Returns:
        [
         {
            "chunk_id": "...",
            "section_id": "...",
            "document_id": "...",
            "text": "...",
            "similarity": 0.82,
            }
        ]

    similarity_score ∈ [-1, 1]
    (cosine similarity)
    """

    # Embed query using unified embedder
    query_embedding = _embedder.embed([query])

    distances, indices = _index.search(
        np.array(query_embedding, dtype="float32"),
        k,
    )

    results: List[Dict] = []
    allowed_document_ids: List[str] | None = None
    length_of_allowed_document_ids = 0
    
    for idx, distance in zip(indices[0], distances[0]):
        if idx == -1:
            continue

        similarity = float(distance)
        chunk = _chunks[idx]

    # 🔥 STEP 34: Document-level filtering
        if allowed_document_ids is not None:
            if chunk["document_id"] not in allowed_document_ids:
                length_of_allowed_document_ids += 1
                print(length_of_allowed_document_ids, "skipped due to document filter")
                continue

        results.append({
            "chunk_id": _chunks[idx]["chunk_id"],
            "similarity": similarity,
            "text": _chunks[idx]["text"],
            "section_id": _chunks[idx]["section_id"],
            "document_id": _chunks[idx]["document_id"],
        })

    return results

def retrieve_context_structured(
    query: str,
    k: int = 4,
) -> List[Dict[str, str]]:
    """
    Structured retrieval for evaluation (STEP 18).

    Returns:
        [
            {
                "id": str,
                "text": str
            },
            ...
        ]
    """

    # Embed query
    query_embedding = _embedder.embed([query])

    distances, indices = _index.search(
        np.array(query_embedding, dtype="float32"),
        k,
    )

    results: List[Dict[str, str]] = []

    for idx in indices[0]:
        if idx == -1:
            continue

        chunk = _chunks[idx]

        results.append(
            {
                "id": chunk["chunk_id"],
                "text": chunk["text"],
            }
        )

    return results