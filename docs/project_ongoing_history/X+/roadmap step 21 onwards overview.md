**Berlin, Germany — 1 February 2026, 15:18 CET**

Perfect — below is the **updated, final `.md` roadmap**, with **Phase 2 / Phase 3 explicitly capturing multi-format ingestion** (`.pdf`, `.docx`, etc.), while keeping the **prototype roadmap clean and honest**.

This version is **review-ready** and defensible.

You can replace the earlier file entirely with this.

---

```md
# Post–STEP 20 Roadmap  
## Local, Grounded RAG System — Prototype & Beyond

---

## 1. Current Status (What Is Already Completed)

### ✅ STEP 20 — Safe, Grounded RAG Core (COMPLETED)

The system has crossed the **trust boundary**.

**Completed capabilities:**
- Deterministic retrieval → reranking → gating → answering
- Explicit relevance thresholds
- Enforced “I don’t know” responses
- Confidence object with rationale
- Source-aware retrieval (internal corpus)
- FakeLLM + deterministic test harness
- Clean separation of concerns
- Shared core across CLI / Web / GUI
- Dockerized, reproducible runtime

**Positioning:**
> The system is no longer a demo RAG.  
> It is a *defensible, inspectable, grounded assistant core*.

---

## 2. Core Runtime Flow (As Implemented)

```

User Query
│
▼
Query Normalization
│
▼
Vector Retrieval (Top-K)
│
▼
Reranking (Cross / Heuristic)
│
▼
Relevance Gating
│     ├─ insufficient → deterministic "I don't know"
│     └─ sufficient
▼
Prompt Assembly (Context + Scores)
│
▼
LLM Invocation
│
▼
Answer + Confidence + Rationale

```

---

## 3. Prototype Scope Constraint — Data Ingestion

### ⚠️ Explicit Prototype Constraint

**Current supported input format:**
- `.txt` files only

**Assumptions:**
- UTF-8 encoded
- Pre-cleaned, text-only content
- No layout, tables, or embedded media

This constraint is **intentional** and allows:
- deterministic chunking
- stable retrieval evaluation
- meaningful confidence calibration
- isolation of RAG correctness from ingestion noise

> Multi-format ingestion is **not missing work** — it is **explicitly deferred**.

---

## 4. Remaining Steps to Complete the Prototype

> 🔢 Remaining prototype steps: **4**  
> 🧱 Overall prototype completion: **~80–85%**

---

### STEP 21 — Confidence Telemetry & Logging

**Goal**  
Make confidence and grounding **observable over time**, not just per query.

**Scope**
- Structured per-query logs
- Retrieval scores, reranking results, gating decision
- Final confidence + rationale
- Debug trace for audits and analysis

---

### STEP 22 — Explainability & Provenance Enrichment  
*(Per-Document / Per-Section Confidence)*

**Goal**  
Explain *why* an answer is confident and *which sources contribute*.

**Scope**
- Per-document confidence attribution
- Optional per-section / chunk contribution
- Source exposure toggle (on/off)
- Expanded, human-readable rationales

---

### STEP 23 — Confidence-Driven Human Review  
**+ Mutation / Adversarial Testing**

**Goal**  
Introduce controlled human-in-the-loop handling for uncertainty.

**Scope**
- Flag low / borderline confidence answers
- Route for manual review or escalation
- Mutation & adversarial tests:
  - query perturbations
  - misleading phrasing
  - near-threshold retrieval cases

---

### STEP 24 — UX & API Exposure Hardening

**Goal**  
Expose the system safely and consistently across interfaces.

**Scope**
- Unified response schema
- Consistent “no answer” behavior
- Confidence always visible
- API surface stabilization
- CLI / Web / GUI parity

---

## 5. Phase 2 — Ingestion Expansion (Post-Prototype)

> **This phase introduces complexity deliberately excluded from the prototype.**

### PHASE 2A — Multi-Format Parsing

**Formats**
- PDF (`.pdf`)
- Word (`.docx`)
- PowerPoint (`.pptx`)
- Emails (`.eml`, `.msg`)

**Includes**
- Format-specific parsers
- Text extraction validation
- Parser failure handling

---

### PHASE 2B — Layout-Aware Chunking

**Scope**
- Section-aware chunking
- Page and heading preservation
- Table and list handling
- Metadata enrichment from structure

---

### PHASE 2C — Ingestion Quality Evaluation

**Scope**
- Parser accuracy metrics
- Chunk coherence checks
- Retrieval quality before vs after ingestion
- Confidence impact analysis

---

## 6. Phase 3 — Production & Scale (Explicitly Out of Prototype)

These items are **intentionally excluded** from prototype scope.

### Phase 3 Capabilities
- SharePoint / OneDrive connectors
- Auth + roles (per-corpus access)
- Queueing & scheduling (fairness, long queries)
- Multi-user UI
- Internet research agent
- Backup automation
- Long-term observability dashboards
- systemd-level service packaging

---

## 7. Final, Unambiguous Status

> 🔢 Remaining prototype steps: **4**  
> 🧱 Completion: **~80–85%**  
> ✅ Core system: **safe, grounded, and defensible**

After STEP 24, the system can be accurately described as:

> **A local-first, document-grounded AI prototype with explicit trust controls, explainability, and human-in-the-loop readiness.**

Multi-format ingestion and operational scale follow in **Phase 2 and Phase 3 by design**, not omission.

---
```

---

### Why this version is strong

* Makes `.txt`-only support **explicit, justified, and intentional**
* Prevents reviewers from calling it a “missing feature”
* Cleanly separates **AI correctness** from **ingestion complexity**
* Aligns perfectly with how senior architects reason about risk

If you want next, I can:

* generate **Phase 2 ingestion STEP files**, or
* help you prepare a **final prototype sign-off / review note** using this roadmap.

Just tell me the next step.
