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


A. Core & Runtime
B. Data Ingestion & Parsing
C. Text Processing & Chunking
D. Embeddings
E. Vector Storage
F. LLM Inference
G. Application & Interface
H. Utilities & Tooling
