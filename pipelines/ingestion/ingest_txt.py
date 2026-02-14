# pipelines/ingestion/ingest_txt.py

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
import uuid

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

files = []
documents = []
sections = []
statuses = []


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def ingest_txt(path: Path, category: str):
    file_id = sha256(path)

    files.append({
        "file_id": file_id,
        "path": str(path),
        "filename": path.name,
        "extension": ".txt",
        "category": category,
        "size_bytes": path.stat().st_size,
        "last_modified": path.stat().st_mtime,
        "checksum_sha256": file_id,
    })

    document_id = str(uuid.uuid4())

    documents.append({
        "document_id": document_id,
        "file_id": file_id,
        "document_name": path.stem,
        "document_type": "other",
        "category": category,
        "version": None,
        "language": "en",
        "source_system": "local_fs",
        "ingested_at": now(),
    })

    text = path.read_text(encoding="utf-8").strip()

    if text:
        sections.append({
            "section_id": str(uuid.uuid4()),
            "document_id": document_id,
            "section_title": path.stem,
            "section_path": path.stem,
            "order_index": 0,
            "text": text,
            "page_start": None,
            "page_end": None,
            "paragraph_start": None,
            "paragraph_end": None,
            "char_start": 0,
            "char_end": len(text),
        })

    statuses.append({
        "entity_type": "document",
        "entity_id": document_id,
        "status": "success",
        "messages": [],
        "timestamp": now(),
    })


def main():
    for category_dir in RAW_DIR.iterdir():
        if not category_dir.is_dir():
            continue

        for txt in category_dir.rglob("*.txt"):
            ingest_txt(txt, category_dir.name)

    (OUT_DIR / "files.json").write_text(json.dumps(files, indent=2))
    (OUT_DIR / "documents.json").write_text(json.dumps(documents, indent=2))
    (OUT_DIR / "sections.json").write_text(json.dumps(sections, indent=2))
    (OUT_DIR / "ingestion_status.json").write_text(json.dumps(statuses, indent=2))


if __name__ == "__main__":
    main()
