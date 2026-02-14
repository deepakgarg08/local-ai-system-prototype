# Local AI System – Complete Architecture Overview

## System Type

Local-first Retrieval-Augmented Generation (RAG) platform
with retrieval gating, reranking, confidence calibration,
evaluation framework, and observability.

---

# 1. Core Runtime Flow

User Query
    ↓
Query Normalization
    ↓
Retrieval (FAISS / Hybrid / BM25)
    ↓
Optional Reranking
    ↓
Relevance Scoring
    ↓
Score Gate (Threshold Enforcement)
    ↓
Prompt Assembly
    ↓
LLM Call
    ↓
Confidence Estimation
    ↓
Answer Formatting
    ↓
Structured Logging

---

# 2. Folder Responsibilities

## /pipelines

Contains all production logic.

### ingestion/
- Reads raw files
- Converts to text
- Prepares documents

### chunking/
- Splits documents into sections
- Adds metadata

### embeddings/
- Embeds chunks
- Builds FAISS index

### retrieval/
- Executes vector search
- Returns top-k

### reranking/
- Cross-encoder
- LLM-based rerankers

### retrieval_quality/
- Hybrid retrieval
- Metadata boosting
- Ranking optimization

### gating/
- Score-based gating
- Blocks low relevance queries

### prompting/
- Prompt assembly
- Confidence prompt builder

### confidence/
- Calibration
- Scoring
- Confidence model

### query/
- End-to-end run_rag orchestration
- Relevance evaluation
- Eligibility logic

---

# 3. /evaluation

Offline evaluation framework:

- Golden queries
- Relevance judgments
- Precision, recall, MRR
- Retrieval regression tests

---

# 4. /analysis

Research + monitoring tools:

- Threshold calibration
- Drift monitoring
- Manual entrypoint detection

Not runtime logic.

---

# 5. /observability

Central structured logging API.
Defines event schema and logger.

---

# 6. /telemetry

Confidence and validation event logging.

---

# 7. /configs

System configuration versioning.
Threshold history.
Active runtime config.

---

# 8. /app

User interfaces:

- CLI
- API (FastAPI)
- Web

---

# 9. /tools

Operational scripts:
- Health checks
- Threshold promotion
- Calibration runs

---

# 10. /experiments

Research-only retrieval experiments.
Not production path.

---

# 11. /logs

Structured JSONL runtime events.
Used for:
- Auditing
- Drift detection
- Regression tracking

---

# Architectural Philosophy

1. Offline indexing is isolated.
2. Retrieval and gating are deterministic.
3. LLM is only called after eligibility passes.
4. Confidence is modeled explicitly.
5. All major decisions are logged.
6. Evaluation is reproducible.
7. Config is versioned.

---

# Known Structural Improvement Areas

- Consolidate retrieval + retrieval_quality
- Unify logging (observability + telemetry)
- Clarify orchestration layer
- Reduce duplication in prompt builders
