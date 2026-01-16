import faiss
import json
from pathlib import Path
from typing import List, Dict


class FaissIndexer:
    def __init__(self, dim: int, index_path: str, meta_path: str):
        self.index_path = Path(index_path)
        self.meta_path = Path(meta_path)
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: List[Dict] = []

    def add(self, embeddings, metadatas: List[Dict]):
        self.index.add(embeddings)
        self.metadata.extend(metadatas)

    def save(self):
        faiss.write_index(self.index, str(self.index_path))
        with open(self.meta_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def load(self):
        self.index = faiss.read_index(str(self.index_path))
        with open(self.meta_path) as f:
            self.metadata = json.load(f)
