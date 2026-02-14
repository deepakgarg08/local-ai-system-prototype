import json
import uuid
from datetime import datetime
from pathlib import Path

from pytz import timezone

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

SECTIONS_PATH = DATA_DIR / "sections.json"
OUT_PATH = DATA_DIR / "chunks.json"


TARGET_CHARS = 1000
OVERLAP_CHARS = 150

def now():
    return datetime.now(timezone.utc).isoformat()


def split_text(text: str):
    """
    Split text into chunks with overlap.
    Prefer paragraph boundaries; fall back to char windows.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []

    current = ""
    for p in paragraphs:
        if len(current) + len(p) + 2 <= TARGET_CHARS:
            current = f"{current}\n\n{p}".strip()
        else:
            if current:
                chunks.append(current)
            current = p

    if current:
        chunks.append(current)

    # Apply overlap if needed
    final_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            final_chunks.append(chunk)
        else:
            prev = final_chunks[-1]
            overlap = prev[-OVERLAP_CHARS:] if len(prev) > OVERLAP_CHARS else prev
            final_chunks.append(f"{overlap}{chunk}")

    return final_chunks


def main():
    sections = json.loads(SECTIONS_PATH.read_text())
    chunks = []

    for section in sections:
        text = section["text"].strip()
        if not text:
            continue

        split_chunks = split_text(text)

        for idx, chunk_text in enumerate(split_chunks):
            chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "section_id": section["section_id"],
                "document_id": section["document_id"],
                "chunk_index": idx,
                "text": chunk_text,
                "char_start": 0,
                "char_end": len(chunk_text),

                # denormalized metadata for fast retrieval & citation
                "document_name": section.get("document_name"),
                "section_title": section.get("section_title"),
                "section_path": section.get("section_path"),
                "page_start": section.get("page_start"),
                "page_end": section.get("page_end"),
                "category": section.get("category"),

                "created_at": now(),
                "pipeline_version": "chunking_v1",
            })

    OUT_PATH.write_text(json.dumps(chunks, indent=2))


if __name__ == "__main__":
    main()
