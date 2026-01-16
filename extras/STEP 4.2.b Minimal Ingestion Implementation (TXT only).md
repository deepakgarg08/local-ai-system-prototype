**📅 14 January 2026, 18:19 (Berlin time)**

Perfect. Now we move from **design → reality**, but in a **controlled, minimal way**.

This is **STEP 4b — Minimal Ingestion Implementation (TXT only)**
✔ real code
✔ aligned with the schemas you defined
✔ still no AI, no embeddings, no vectors

---

# STEP 4b — Minimal Ingestion Pipeline (TXT Only)

## Scope (Very Important)

We will implement **only**:

* `.txt` files
* local filesystem
* flat text + headings
* JSON outputs

This is **intentional**. TXT is the *reference implementation* for all other formats.

---

## 1. What You Will Build in This Step

### Input

```
data/raw/**/**/*.txt
```

### Output

```
data/processed/
├── files.json
├── documents.json
├── sections.json
└── ingestion_status.json
```

Each file will follow the **schemas from Step 4a**.

---

## 2. Create the Ingestion Module Skeleton

From project root:

```bash
mkdir -p pipelines/ingestion
touch pipelines/ingestion/__init__.py
nano pipelines/ingestion/ingest_txt.py
```

---

## 3. Responsibilities of `ingest_txt.py`

This script will:

1. Scan `data/raw/`
2. Detect `.txt` files
3. Create `FileRecord`
4. Create `DocumentRecord`
5. Split text into **sections**
6. Write JSON artifacts

---

## 4. Minimal Sectioning Rule (For Now)

We use a **simple, deterministic rule**:

* A line is a **section title** if:

  * it is not empty
  * AND it has no indentation
  * AND the next line is not empty

Example:

```
Company Overview
ACME Systems GmbH is a fictional company...
```

This is **good enough** for a first pipeline.

---

## 5. Minimal Implementation (Core Logic)

Put this into `pipelines/ingestion/ingest_txt.py`:

```python
import json
import hashlib
from pathlib import Path
from datetime import datetime
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
    return datetime.utcnow().isoformat()


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
```

---

## 6. Run the Ingestion

Make sure you have at least one `.txt` file in `data/raw/...`.

Then run:

```bash
python pipelines/ingestion/ingest_txt.py
```

Check output:

```bash
ls data/processed
```

You should see all four JSON files.

---

## 7. Validate the Result (Very Important)

Open one file:

```bash
less data/processed/sections.json
```

You should see:

* section titles
* section text
* document linkage
* stable IDs

If this looks correct → **Step 4b is successful**.

---

## 8. What You Have Achieved (This Is Big)

You now have:

* a real ingestion pipeline
* enterprise-style schemas
* traceable sections
* reproducible processing
* zero AI complexity

This is **exactly how serious RAG systems start**.

---

## 9. What We Still Did NOT Do (Correctly)

❌ PDFs
❌ DOCX
❌ Chunking
❌ Embeddings
❌ Vector DB
❌ LLM

Those come *after* this foundation.

---

## Next Step (Natural Progression)

👉 **STEP 5 — Chunking Strategy & Chunk Schema**
We decide:

* how sections become chunks
* how chunk size is chosen
* how citations are preserved

When ready, say:

> **“Proceed to Step 5”**

You are building this the *right way*.
