local-ai-system-prototype/
│
├── docs/                     → architecture notes, design decisions, step-by-step docs
│                              (source of truth for system design)
│
├── data/
│   ├── raw/                  → original input documents (PDF, DOCX, TXT)
│                              (never modified after ingestion)
│   ├── processed/            → cleaned, normalized, and chunked text
│                              (output of ingestion + chunking pipelines)
│   └── indexes/              → build-time artifacts for retrieval
│                              (FAISS index files, chunks.json, metadata snapshots)
│
├── llms/                     → LLM capability layer (CORE INFRASTRUCTURE)
│   ├── base.py               → abstract BaseLLM contract (single source of truth)
│   └── ollama.py             → local LLM implementation using Ollama
│                              (real inference, no placeholders)
│
├── pipelines/                → execution pipelines (build-time + query-time)
│   ├── indexing/             → offline pipelines to build embeddings and indexes
│   ├── query/                → runtime query pipelines (retrieval, prompt assembly)
│   │   └── retriever.py      → retrieves relevant chunks from vector index
│   └── llm/                  → temporary execution/tests related to LLM usage
│                              (consumes llms/, does not define LLMs)
│
├── models/                   → local model files (future)
│                              (downloaded LLMs, embedding models, weights)
│
├── vectorstores/             → semantic storage backends (future)
│                              (FAISS, hybrid search, BM25 + vectors)
│
├── app/                      → application layer (future)
│                              (API server, UI, request handling)
│
├── configs/                  → configuration & environment settings (future)
│                              (model selection, paths, runtime toggles)
│
├── scripts/                  → admin and utility scripts (future)
│                              (rebuild index, health checks, maintenance tasks)
│
├── tests/                    → test scaffolding
│                              (unit, integration, retrieval-quality tests)
│
├── logs/                     → runtime and audit logs
│                              (query traces, errors, performance metrics)
│
├── pyproject.toml            → project metadata, dependencies, packaging config
├── README.md                 → project overview and usage instructions
└── .venv/                    → Python virtual environment (local, not committed)




docs/
├── README.md
│
├── architecture/
│   ├── overview.md
│   ├── directory_layout.md
│   ├── data_flow.md
│   ├── retrieval_flow.md
│   ├── build_time_vs_query_time.md
│   └── failure_modes.md
│
├── steps/
│   ├── step_00_project_setup.md
│   ├── step_01_data_ingestion.md
│   ├── step_02_sectioning.md
│   ├── step_03_chunking.md
│   ├── step_04_embedding_generation.md
│   ├── step_05_faiss_index_building.md
│   ├── step_06_index_validation.md
│   ├── step_07_query_embedding.md
│   ├── step_08_fake_retrieval_removal.md
│   ├── step_09_real_faiss_retrieval.md
│   ├── step_10_prompt_assembly.md
│   ├── step_11_local_llm_inference.md
│   ├── step_12_reranking_and_mmr.md
│   ├── step_13_hybrid_search_bm25_faiss.md
│   └── step_14_end_to_end_pipeline.md
│
├── pipelines/
│   ├── ingestion.md
│   ├── sectioning.md
│   ├── chunking.md
│   ├── embeddings.md
│   ├── indexing.md
│   ├── retrieval.md
│   ├── prompt_builder.md
│   ├── llm_client.md
│   └── orchestration.md
│
├── data/
│   ├── raw_data.md
│   ├── processed_data.md
│   ├── sections_schema.md
│   ├── chunks_schema.md
│   ├── indexes.md
│   ├── metadata_schema.md
│   └── versioning_strategy.md
│
├── configs/
│   ├── path_resolution.md
│   ├── model_selection.md
│   ├── embedding_settings.md
│   ├── faiss_settings.md
│   ├── llm_runtime_settings.md
│   └── environment_variables.md
│
├── decisions/
│   ├── why_faiss.md
│   ├── why_sentence_transformers.md
│   ├── why_list_based_metadata.md
│   ├── normalization_strategy.md
│   ├── cpu_vs_gpu_tradeoffs.md
│   └── local_first_design.md
│
├── troubleshooting/
│   ├── common_errors.md
│   ├── faiss_runtime_errors.md
│   ├── embedding_mismatches.md
│   ├── metadata_alignment_issues.md
│   ├── performance_bottlenecks.md
│   └── debugging_checklist.md
│
├── testing/
│   ├── test_strategy.md
│   ├── unit_tests.md
│   ├── integration_tests.md
│   ├── retrieval_quality_tests.md
│   └── regression_tests.md
│
├── security/
│   ├── local_data_safety.md
│   ├── model_integrity.md
│   └── dependency_risks.md
│
└── glossary/
    ├── terminology.md
    ├── vector_search_terms.md
    └── rag_concepts.md

local-ai-system-prototype/
│
├── docs/            → architecture notes, diagrams, decisions
├── data/
│   ├── raw/         → original documents (PDFs, DOCX, TXT)
│   ├── processed/   → cleaned & chunked text (later)
│   └── indexes/     → metadata snapshots
│
├── pipelines/       → ETL, ingestion, updates (future)
├── models/          → local LLMs, embedding models (future)
├── vectorstores/    → semantic indexes (future)
│
├── app/             → UI + request handling (future)
├── configs/         → configuration & environment settings
├── scripts/         → admin / utility scripts
├── tests/           → test scaffolding
└── logs/            → runtime & audit logs