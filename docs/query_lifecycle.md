┌──────────────────┐
│   User Query     │
│ "Explain caching │
│  vs indexing"    │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│ 1️⃣ Exact Query Cache     │
│ (string / hash lookup)  │
└────────┬─────────────────┘
         │ hit?
         ├── YES → return cached answer ✅
         │
         ▼ NO
┌──────────────────────────┐
│ 2️⃣ Query Rewriting LLM   │  ← Approach B (optional)
│ - clarify intent         │
│ - add missing context    │
│ - normalize phrasing     │
└────────┬─────────────────┘
         │ rewritten query
         ▼
┌──────────────────────────┐
│ 3️⃣ Rewritten Query Cache │
│ (hash or embedding match)│
└────────┬─────────────────┘
         │ hit?
         ├── YES → reuse rewritten intent
         │
         ▼ NO
┌──────────────────────────┐
│ 4️⃣ Query Embedding       │
│ (embedding model)        │
└────────┬─────────────────┘
         │ vector
         ▼
┌──────────────────────────┐
│ 5️⃣ Semantic Cache        │
│ (cosine similarity ≥ τ)  │
└────────┬─────────────────┘
         │ hit?
         ├── YES → reuse retrieval result
         │
         ▼ NO
┌──────────────────────────┐
│ 6️⃣ Vector Database       │
│ (cosine similarity)      │
│ → retrieve top-k chunks  │
└────────┬─────────────────┘
         │ chunks
         ▼
┌──────────────────────────┐
│ 7️⃣ Prompt Assembly      │  ← STEP 10
│ - system instructions   │
│ - retrieved context     │
│ - user intent           │
└────────┬─────────────────┘
         │ full prompt
         ▼
┌──────────────────────────┐
│ 8️⃣ LLM Generation       │
│ (local / remote model)  │
└────────┬─────────────────┘
         │ answer
         ▼
┌──────────────────────────┐
│ 9️⃣ Response Cache       │
│ (optional, TTL-based)   │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────┐
│   Final Answer   │
└──────────────────┘
