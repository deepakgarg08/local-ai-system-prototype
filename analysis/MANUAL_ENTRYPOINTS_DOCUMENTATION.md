# Manual Entrypoint Documentation

## llms/check_llm_working.py
**Category:** other

### Description
_No module-level docstring found._

---

## pipelines/run_rag_once.py
**Category:** pipeline

### Description
_No module-level docstring found._

---

## pipelines/chunking/chunk_sections.py
**Category:** pipeline

### Description
_No module-level docstring found._

---

## pipelines/indexing/build_index.py
**Category:** pipeline

### Description
_No module-level docstring found._

---

## pipelines/ingestion/ingest_txt.py
**Category:** pipeline

### Description
_No module-level docstring found._

---

## pipelines/prompting/prompt_builder.py
**Category:** pipeline

### Description
_No module-level docstring found._

---

## pipelines/retrieval/faiss_search.py
**Category:** pipeline

### Description
_No module-level docstring found._

---

## pipelines/retrieval/scoring.py
**Category:** pipeline

### Description
_No module-level docstring found._

---

## scripts/cleanup_empty_folders.py
**Category:** runtime_script

### Description
_No module-level docstring found._

---

## scripts/run_query.py
**Category:** runtime_script

### Description
CLI entry point for the local RAG system.

Responsibilities:
- Call run_rag (single orchestration authority)
- Convert RAGResult into human-readable output
- Display confidence and rationale

---

## scripts/run_query_debug_script.py
**Category:** runtime_script

### Description
_No module-level docstring found._

---

## tools/check_llm_health.py
**Category:** admin

### Description
_No module-level docstring found._

---

## tools/detect_manual_entrypoints.py
**Category:** admin

### Description
_No module-level docstring found._

---

## tools/promote_threshold.py
**Category:** admin

### Description
_No module-level docstring found._

---

## tools/run_confidence_calibration.py
**Category:** admin

### Description
Runs the full confidence calibration workflow.
It mimics the MakeFile, either run MakeFile or this script.

Covers:
- STEP 21 — Telemetry generation
- STEP 22 — Telemetry analysis
- STEP 23 — Threshold calibration

---

## XTRAS/OLD_DISCARDED/checkllmspeed.py
**Category:** archived

### Description
_No module-level docstring found._

---

## XTRAS/OLD_DISCARDED/run_query.py
**Category:** archived

### Description
End-to-end query pipeline:
User query → retrieval → prompt → Ollama → answer

---

## analysis/confidence_telemetry_analysis.py
**Category:** analysis

### Description
_No module-level docstring found._

---

## analysis/confidence_threshold_calibration.py
**Category:** analysis

### Description
_No module-level docstring found._

---

## analysis/gate_drift_monitor.py
**Category:** analysis

### Description
_No module-level docstring found._

---

## analysis/gate_threshold_calibration.py
**Category:** analysis

### Description
STEP 31 — Relevance Gate Stability & Threshold Calibration

This script analyzes decision-level RAG logs and evaluates:

1. Similarity distribution
2. Gate pass/fail separation
3. Threshold stability margin
4. Candidate safer thresholds

This script does NOT modify runtime behavior.
It is purely analytical.

---

## app/cli/main.py
**Category:** runtime_entry

### Description
_No module-level docstring found._

---

## evaluation/run_confidence_calibration_set.py
**Category:** evaluation

### Description
_No module-level docstring found._

---

## evaluation/runner/run_retrieval_eval.py
**Category:** evaluation

### Description
_No module-level docstring found._

---
