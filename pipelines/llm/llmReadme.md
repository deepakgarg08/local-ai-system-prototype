Create a single, stable interface that:

Accepts the assembled prompt (from Step 10)

Can call:

✅ Local LLMs (later: llama.cpp, vLLM, Ollama, etc.)

✅ Online LLMs (OpenAI, Anthropic, any API)

Keeps zero coupling with prompt assembly or retrieval

Allows easy swapping of models without touching pipeline logic

🧠 Design Principle (Very Important)

We use the Adapter Pattern.

Prompt (string)
   ↓
LLM Interface (abstract)
   ↓
Concrete Adapter
   ├── Local LLM
   └── Online LLM


The rest of your system never knows which model is used.
pipelines/
└── llm/
    ├── __init__.py
    ├── base.py          ← abstract interface
    ├── local.py         ← local LLM adapter (stub for now)
    └── online.py        ← online LLM adapter (stub for now)
