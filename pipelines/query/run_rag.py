# pipelines/query/run_rag.py

from typing import List, Dict
from dataclasses import dataclass

from pipelines.query.retriever import retrieve_context_with_scores
from pipelines.query.relevance import is_context_relevant
from pipelines.prompting.assemble_prompt import assemble_prompt
from pipelines.confidence.models import ConfidenceReport, RetrievalEvidence
from pipelines.confidence.scorer import score_confidence
from llms.registry import get_llm
from pipelines.query.relevance import MIN_SIMILARITY_THRESHOLD



@dataclass
class RAGResult:
    """
    Structured result returned by the RAG pipeline.

    - answer: generated answer or None if blocked
    - confidence: deterministic confidence assessment
    - sources: retrieval evidence used for generation
    """
    query: str
    answer: str | None
    confidence: ConfidenceReport
    sources: list[RetrievalEvidence]


def run_rag(query: str, top_k: int = 4) -> RAGResult:
    """
    End-to-end RAG execution WITH grounding, confidence, and explainability.

    Flow:
        query
          → retrieve_context_with_scores
          → build retrieval evidence
          → grounding and confidence scoring
          → relevance (grounding) check
          → assemble_prompt
          → unified LLM
          → structured RAGResult
    """

    if not query or not query.strip():
        raise ValueError("Query must be a non-empty string")

    # 1. Retrieve context with similarity scores
    retrieved = retrieve_context_with_scores(query, k=top_k)

    # 2. Build retrieval evidence objects (STEP 15)
    evidence: list[RetrievalEvidence] = [
        RetrievalEvidence(
            chunk_id=f"chunk_{i}",
            source_document="unknown",  # filled later when metadata is available
            similarity_score=score,
            chunk_text=text,
        )
        for i, (text, score) in enumerate(retrieved)
    ]

    # 3. Compute deterministic confidence BEFORE LLM call
    confidence = score_confidence(
        evidence=evidence,
        similarity_threshold=MIN_SIMILARITY_THRESHOLD
    )

    # 4. Enforce grounding (hard gate)
    if not is_context_relevant(retrieved):
        return RAGResult(
            query=query,
            answer=None,
            confidence=confidence,
            sources=[]
        )

    # 5. Prepare context for prompt assembly (strip metadata)
    context_chunks: List[Dict] = [
        {"text": e.chunk_text}
        for e in evidence
    ]

    # 6. Assemble prompt (LLM never sees confidence or scores)
    prompt = assemble_prompt(
        query=query,
        context_chunks=context_chunks,
        system_instruction=None,
    )

    # 7. Generate answer
    llm = get_llm()
    answer = llm.generate(prompt)

    # 8. Return structured, explainable result
    return RAGResult(
        query=query,
        answer=answer,
        confidence=confidence,
        sources=evidence
    )
