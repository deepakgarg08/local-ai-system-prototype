"""
STEP 34 — Document-Level FAISS Index

Builds a lightweight FAISS index over documents
(using title + optional summary).
"""

import json
import numpy as np
import faiss
from pathlib import Path

from pipelines.embeddings.embedder import Embedder

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
INDEX_DIR = PROJECT_ROOT / "data" / "indexes" / "documents"

DOCUMENTS_PATH = PROCESSED_DIR / "documents.json"

DOC_INDEX_PATH = INDEX_DIR / "doc_faiss.index"
DOC_META_PATH = INDEX_DIR / "doc_metadata.json"


def main():
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)

    if not documents:
        raise ValueError("No documents found.")

    texts = []
    metadata = []

    for doc in documents:
        text = f"{doc['document_name']} {doc.get('summary', '')}"
        texts.append(text)
        metadata.append({
            "document_id": doc["document_id"],
            "document_name": doc["document_name"],
        })

    embedder = Embedder()
    embeddings = embedder.embed(texts)
    embeddings = np.asarray(embeddings, dtype="float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, str(DOC_INDEX_PATH))

    with open(DOC_META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Document index built.")
    print(f"Documents indexed: {len(metadata)}")
    print(f"Embedding dim: {dim}")


if __name__ == "__main__":
    main()
