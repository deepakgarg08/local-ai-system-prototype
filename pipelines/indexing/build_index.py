import json
import numpy as np
from pathlib import Path

from pipelines.embeddings.embedder import Embedder
from pipelines.embeddings.indexer import FaissIndexer


# ============================================================
# Canonical project root (same pattern as chunking pipeline)
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ============================================================
# Data paths
# ============================================================
DATA_DIR = PROJECT_ROOT / "data" / "processed"
INDEX_DIR = PROJECT_ROOT / "data" / "indexes"

SECTIONS_PATH = DATA_DIR / "sections.json"

INDEX_PATH = INDEX_DIR / "faiss.index"
META_PATH = INDEX_DIR / "metadata.json"


def main():
    # --------------------------------------------------------
    # Sanity checks
    # --------------------------------------------------------
    if not SECTIONS_PATH.exists():
        raise FileNotFoundError(
            f"Chunk file not found: {SECTIONS_PATH}\n"
            "Make sure STEP 6b (chunking) has been run."
        )

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Load chunked data
    # --------------------------------------------------------
    print("Loading chunked sections...")
    with open(SECTIONS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        raise ValueError("No chunks found in sections.json")

    print(f"Loaded {len(chunks)} chunks")

    # --------------------------------------------------------
    # Prepare texts for embedding
    # --------------------------------------------------------
    texts = [chunk["text"] for chunk in chunks]

    # --------------------------------------------------------
    # Embed texts
    # --------------------------------------------------------
    print("Embedding chunks...")
    embedder = Embedder()
    embeddings = embedder.embed(texts)

    embeddings = np.asarray(embeddings, dtype="float32")
    dim = embeddings.shape[1]

    print(f"Embedding dimension: {dim}")

    # --------------------------------------------------------
    # Build FAISS index
    # --------------------------------------------------------
    indexer = FaissIndexer(
        dim=dim,
        index_path=str(INDEX_PATH),
        meta_path=str(META_PATH),
    )

    indexer.add(embeddings, chunks)

    # --------------------------------------------------------
    # Persist index + metadata
    # --------------------------------------------------------
    indexer.save()

    print("Indexing complete.")
    print(f"FAISS index written to: {INDEX_PATH}")
    print(f"Metadata written to:   {META_PATH}")


if __name__ == "__main__":
    main()
