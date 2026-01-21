import sys
from pathlib import Path

# --- Ensure project root is on PYTHONPATH ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from pydantic import BaseModel
from pipelines.query.run_rag import run_rag
import os
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

print(os.getenv("LLM_PROVIDER"))
print(os.getenv("LLM_MODEL"))

app = FastAPI(
    title="Local AI Assistant API",
    version="20.9",
    description="Document-grounded RAG API",
)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class QueryResponse(BaseModel):
    query: str
    answer: str | None
    confidence_level: str
    rationale: list[str]


@app.post("/query", response_model=QueryResponse)
def query_rag(req: QueryRequest):
    result = run_rag(query=req.query, top_k=req.top_k)

    return QueryResponse(
        query=req.query,
        answer=result.answer,
        confidence_level=result.confidence.confidence_level,
        rationale=result.confidence.rationale,
    )
