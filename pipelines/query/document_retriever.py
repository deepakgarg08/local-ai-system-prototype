"""
STEP 34 — Document-Level Retrieval
"""

import json
import faiss
import numpy as np
from pathlib import Path
from typing import List

from pipelines.embeddings.embedder import Embedder

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INDEX_DIR = PROJECT_ROOT / "data" / "indexes" / "documents"

DOC_INDEX_PATH = INDEX_DIR / "doc_faiss.index"
DOC_META_PATH = INDEX_DIR / "doc_metadata.json"

_embedder = Embedder()

_index = None
_metadata = None


def _load_index():
    global _index, _metadata

    if _index is None:
        if not DOC_INDEX_PATH.exists():
            raise FileNotFoundError(
                f"Document index not found: {DOC_INDEX_PATH}\n"
                "Run STEP 34 indexing first."
            )

        _index = faiss.read_index(str(DOC_INDEX_PATH))

        with open(DOC_META_PATH, "r", encoding="utf-8") as f:
            _metadata = json.load(f)


def retrieve_top_documents(query: str, top_n: int = 3) -> List[str]:
    _load_index()

    query_embedding = _embedder.embed([query])
    distances, indices = _index.search(
        np.array(query_embedding, dtype="float32"),
        top_n
    )

    results = []

    for idx in indices[0]:
        if idx == -1:
            continue
        results.append(_metadata[idx]["document_id"])

    return results
