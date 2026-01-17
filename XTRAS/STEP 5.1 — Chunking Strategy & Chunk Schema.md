**📅 14 January 2026, 18:33 (Berlin time)**

## STEP 5 — Chunking Strategy & Chunk Schema

*(Technical design, no model/vector implementation yet)*

This step defines **how sections (from Step 4) become retrieval-ready chunks** **without losing citations**.
It is **explicitly required** by the uploaded project PDF because answers must be **traceable to document/section/page** and reviewed by humans .

---

## 1) Why Chunking Exists (in *this* project)

* **Retrieval accuracy:** Search works on chunks, not whole documents.
* **Citation safety:** Chunks must *inherit* section metadata.
* **Human review:** Every answer must point back to a verifiable source.

> Chunking is a *technical compromise* between recall, precision, and traceability.

---

## 2) Golden Rules (Non-Negotiable)

1. **Never chunk raw files** → only chunk **SectionRecords**
2. **Chunks never stand alone** → each chunk references its **section_id**
3. **Metadata is inherited, not re-created**
4. **Chunk boundaries must be deterministic** (reproducible)

---

## 3) Chunking Strategy (Deterministic & Simple)

### Primary unit

* Input: `SectionRecord.text`
* Output: multiple `ChunkRecord`s

### Size policy (initial, conservative)

* **Target size:** ~800–1,200 characters
* **Overlap:** 100–150 characters (to preserve context)
* **Hard limits:** never exceed section boundaries

### Split logic (priority order)

1. Paragraph breaks
2. Sentence boundaries
3. Character count fallback

This keeps chunks **semantically coherent** while staying index-friendly.

---

## 4) Chunk Schema (What You Will Persist)

### `ChunkRecord`

```text
chunk_id           : string (stable UUID)
section_id         : string (FK)
document_id        : string (FK)

chunk_index        : integer
text               : string

char_start         : integer
char_end           : integer

# inherited / denormalized for fast access
document_name      : string
section_title      : string
section_path       : string
page_start         : integer | null
page_end           : integer | null
category            : enum [knowledge, contracts, specs, training]

created_at         : timestamp
pipeline_version   : string
```

### Why denormalize?

* Faster retrieval
* Easier citation assembly
* Cleaner prompts later

---

## 5) Relationship Chain (End-to-End)

```
File
  → Document
     → Section
        → Chunk
           → (later) Embedding
```

**Citations always resolve upward**:
`Chunk → Section → Document → File`

---

## 6) What This Enables Later (Without Rework)

* **RAG answers with citations** (doc + section + page)
* **Cross-version queries** (specs)
* **Role-based filtering** (by category)
* **Re-indexing without re-ingestion**

This is exactly aligned with the PDF’s requirement for **RAG-based retrieval with human control** .

---

## 7) What We Still Do NOT Do (Yet)

* ❌ No embeddings
* ❌ No vector DB
* ❌ No similarity search
* ❌ No prompts/LLMs

Chunking is the **last step before ML**—done correctly, everything after is easier.

---

## 8) Storage (Prototype)

After this step, you’ll add one file:

```
data/processed/
├── files.json
├── documents.json
├── sections.json
├── chunks.json        ← NEW
└── ingestion_status.json
```

---

## Next Step (Clear Choice)

👉 **STEP 5b — Implement Chunking (using existing sections.json)**
We’ll write a small, deterministic chunker and generate `chunks.json`.

When ready, say:

> **“Proceed to Step 5b”**

You’re building a **production-grade RAG foundation**, even on a laptop.


**📅 14 January 2026, 18:36 (Berlin time)**

Short answer: **Yes — conceptually, what we designed *is* a Parent Document Retriever–style chunking strategy.**
But with an **enterprise-grade, citation-safe variant**.

Let me explain precisely, without buzzwords.

---

## 1️⃣ What “Parent Document Retriever” Actually Means

In general terms, **Parent Document Retriever (PDR)** refers to a pattern where:

* **Small chunks** are used for retrieval (search accuracy)
* **Larger parent units** are used for context and citation
* The system never treats chunks as standalone truth

In most tutorials, the hierarchy is:

```
Document → Chunk
```

---

## 2️⃣ What *You* Are Building (More Correct)

Your design is actually **better and stricter** than most PDR examples:

```
File → Document → Section → Chunk
```

Here:

* **Chunk** = retrieval unit
* **Section** = citation & semantic parent
* **Document** = legal / business source of truth
* **File** = physical evidence

This is a **multi-level Parent Retriever**, not the simplistic version.

---

## 3️⃣ Why This *Is* Parent Document Retrieval

Your chunking strategy satisfies all defining properties:

### ✅ Small chunks for retrieval

* 800–1200 chars
* overlap for semantic continuity

### ✅ Parent context preserved

* Every chunk references:

  * `section_id`
  * `document_id`

### ✅ Retrieval ≠ Answer authority

* Retrieval happens at chunk level
* **Answers are grounded at section/document level**

That is **exactly** the Parent Document Retriever idea — done properly.

---

## 4️⃣ How This Differs from “Tutorial PDR”

| Typical tutorial PDR | Your design                 |
| -------------------- | --------------------------- |
| Chunk → parent doc   | Chunk → section → doc       |
| Often loses pages    | Page numbers preserved      |
| Loose metadata       | Strict schemas              |
| Good for demos       | Good for audits & contracts |
| Chatbot-first        | Human-review-first          |

Most tutorials **collapse sections**, which breaks:

* citations
* legal review
* enterprise trust

Your approach does **not**.

---

## 5️⃣ Why This Matters for Your Project (PDF Alignment)

The uploaded project PDF requires:

* document + section references
* human verification
* avoidance of hallucinations
* cross-version specs
* contract traceability

A **naive chunk-only RAG** would violate these requirements.
Your **Parent (Section) → Chunk** model fully satisfies them.

---

## 6️⃣ Correct Terminology You Can Use (Professionally)

If you describe this project, you can accurately say:

> “We use a hierarchical Parent Document Retrieval strategy, where chunks are retrieval units and document sections act as citation parents.”

That is **100% correct**.

---

## 7️⃣ One-Line Conclusion (Very Clear)

> **Yes — this is Parent Document Retriever–style chunking, implemented in a stricter, enterprise-safe form using sections as the true parent unit.**

You understood it correctly.

---

### Next step (when ready)

👉 **STEP 5b — Implement Chunking**

Say:

> **“Proceed to Step 5b”**

And we’ll turn this design into working, deterministic code.

