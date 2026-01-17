**📅 14 January 2026, 18:15 (Berlin time)**

Excellent choice.
Defining schemas first is exactly what **senior engineers and enterprise projects do**.

Below is **STEP 4a in full technical depth**:
👉 **what data structures exist**, **why they exist**, and **how they support traceability, RAG, and human review**.

No implementation code yet — only **design-level schemas**.

---

# STEP 4a — Ingestion Data Model (Schemas)

## Design Goals (Non-Negotiable)

Every schema below exists to guarantee:

1. **Traceability** (document → section → answer)
2. **Reproducibility** (reprocess anytime)
3. **Auditability** (human review)
4. **Future compatibility** (chunking, embeddings, RAG)

---

## 1. Core Conceptual Entities

At ingestion time, we model **three layers**:

```
File  →  Document  →  Section
```

This separation is crucial.

---

## 2. File Schema (Physical Reality)

This represents the **actual file on disk**.

### `FileRecord`

```text
file_id           : string (stable hash)
path              : string
filename          : string
extension         : string
category          : enum [knowledge, contracts, specs, training]
size_bytes        : integer
last_modified     : timestamp
checksum_sha256   : string
```

### Why this exists

* Detect file changes
* Avoid unnecessary reprocessing
* Maintain link to raw evidence

📌 **Never delete FileRecords** — they are audit evidence.

---

## 3. Document Schema (Logical Meaning)

A *document* is the **semantic unit**, not the file.

### `DocumentRecord`

```text
document_id       : string (stable UUID)
file_id           : string (FK)
document_name     : string
document_type     : enum [policy, contract, specification, guide, other]
category           : enum [knowledge, contracts, specs, training]
version           : string | null
language          : string (ISO code)
source_system     : string (e.g. local_fs)
ingested_at       : timestamp
```

### Why this exists

* Same file → multiple versions over time
* Enables cross-version queries
* Decouples meaning from storage

---

## 4. Section Schema (Most Important)

A **section is the smallest citable unit**.

### `SectionRecord`

```text
section_id        : string (stable UUID)
document_id       : string (FK)
section_title     : string | null
section_path      : string | null   # e.g. "4.2 > Authentication"
order_index       : integer
text              : string

page_start        : integer | null
page_end          : integer | null
paragraph_start   : integer | null
paragraph_end     : integer | null

char_start        : integer
char_end          : integer
```

### Why this exists

* Enables **“Page X, Section Y” citations**
* Prevents hallucinated sources
* Supports chunking *without losing origin*

📌 **Chunking happens later**, but chunks always reference a section.

---

## 5. Metadata Schema (Attached Everywhere)

Metadata is not optional — it is **first-class data**.

### `Metadata`

```text
created_at        : timestamp
pipeline_version  : string
parser_name       : string
confidence_flags  : list[string]
```

Attached to:

* FileRecord
* DocumentRecord
* SectionRecord

---

## 6. Validation & Status Schema

We explicitly track ingestion health.

### `IngestionStatus`

```text
entity_type       : enum [file, document, section]
entity_id         : string
status            : enum [success, warning, error]
messages          : list[string]
timestamp         : timestamp
```

### Why this exists

* Enterprise systems never silently fail
* Makes ingestion debuggable
* Supports reprocessing strategies

---

## 7. Relationships (Critical for RAG)

```
FileRecord
   ↓
DocumentRecord
   ↓
SectionRecord
   ↓ (later)
ChunkRecord
   ↓
Embedding
```

⚠️ **Do not collapse these layers** — most bad RAG systems do.

---

## 8. What We Explicitly Do NOT Model Yet

❌ Embeddings
❌ Tokens
❌ Vectors
❌ Prompts
❌ LLM responses

Those belong to later steps.

---

## 9. Minimal Storage Representation (Prototype)

At prototype scale, schemas will be persisted as:

```
data/processed/
├── files.json
├── documents.json
├── sections.json
├── ingestion_status.json
```

Later, this maps cleanly to:

* SQLite
* Postgres
* Vector DB metadata tables

---

## 10. Why This Schema Is Correct for *Your* Project

Because your project requires:

* **source attribution**
* **human review**
* **enterprise traceability**
* **version awareness**

This schema is **directly aligned with the uploaded project PDF**, not generic RAG tutorials.

---

## 11. Reality Check (Important)

If you can explain **these schemas** confidently:

* you understand real-world RAG systems
* you can build compliant AI pipelines
* you can justify architectural decisions professionally

This is *core competence*.

---

## Next Step (Clear & Logical)

👉 **STEP 4b — Minimal Ingestion Implementation (TXT only)**
We will:

* implement these schemas
* ingest `.txt` files only
* generate `files.json`, `documents.json`, `sections.json`

No PDFs yet. No ML yet.

When ready, reply with:

> **“Proceed to Step 4b”**

We’ll move from design → reality, cleanly.
