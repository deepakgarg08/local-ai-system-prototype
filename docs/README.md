local-ai-system-prototype/
│
├── docs/                    # architecture notes, diagrams, decisions
│
├── data/
│   ├── raw/                 # original documents (PDFs, DOCX, TXT)
│   ├── processed/           # cleaned, sectioned, chunked text
│   └── indexes/             # FAISS index + metadata
│
├── pipelines/               # ETL, ingestion, indexing, retrieval
│   ├── ingestion/
│   ├── sectioning/
│   ├── chunking/
│   ├── embeddings/
│   ├── indexing/
│   ├── retrieval/
│   ├── prompting/
│   ├── llm/
│   └── orchestration/
│
├── models/                  # local LLMs, embedding models (future)
│
├── vectorstores/            # semantic stores (FAISS, BM25, hybrid)
│
├── app/                     # UI / API layer (future)
│
├── configs/                 # configuration & environment settings
│
├── scripts/                 # admin / maintenance utilities
│
├── tests/                   # unit + integration tests
│
├── logs/                    # runtime, audit, error logs
│
├── pyproject.toml
├── README.md
└── .gitignore


tests/
├── unit/            # pure logic, deterministic
├── retrieval/       # embeddings + vector store
├── query/           # RAG wiring (mocked LLM)
├── llm_integration/ # REAL LLM (later, optional)
