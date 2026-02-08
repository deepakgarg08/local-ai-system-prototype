# data/registry.py
import json
from pathlib import Path

BASE = Path("data/processed")

with open(BASE / "chunks.json") as f:
    CHUNKS = {c["chunk_id"]: c for c in json.load(f)}

with open(BASE / "sections.json") as f:
    SECTIONS = {s["section_id"]: s for s in json.load(f)}

with open(BASE / "documents.json") as f:
    DOCUMENTS = {d["document_id"]: d for d in json.load(f)}

with open(BASE / "files.json") as f:
    FILES = {f["file_id"]: f for f in json.load(f)}
