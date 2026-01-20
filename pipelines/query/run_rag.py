# pipelines/query/run_rag.py

from typing import List, Dict
from dataclasses import dataclass

# --- Retrieval & relevance ---
from pipelines.query.retriever import retrieve_context_with_scores
from pipelines.query.relevance import (
    is_context_relevant,
    MIN_SIMILARITY_THRESHOLD,
)

# --- Prompting ---
from pipelines.prompting.assemble_prompt import assemble_prompt

# --- Confidence & explainability ---
from pipelines.confidence.models import ConfidenceReport, RetrievalEvidence
from pipelines.confidence.scorer import score_confidence

# --- Gating (post-generation safety) ---
from pipelines.gating.gate import is_answer_allowed

# --- LLM infrastructure ---
from llms.registry import get_llm

# --- Configuration ---
from configs.retrieval import CORPUS_PROFILE  # STEP 17: corpus-aware behavior


@dataclass
class RAGResult:
    """
    Structured result returned by the RAG pipeline.

    This object is intentionally explicit and explainable.
    Nothing is hidden inside free-form text.

    Fields:
        query      : original user query
        answer     : generated answer, or None if blocked by gating
        confidence : deterministic confidence assessment (pre-LLM)
        sources    : retrieval evidence used for grounding & explainability
    """
    query: str
    answer: str | None
    confidence: ConfidenceReport
    sources: list[RetrievalEvidence]


def run_rag(query: str, top_k: int = 4) -> RAGResult:
    """
    End-to-end RAG execution WITH grounding, confidence, and explainability.

    Architectural guarantees:
    - Retrieval happens before any LLM call
    - Confidence is computed deterministically (pre-LLM)
    - LLM never sees similarity scores or confidence
    - Multiple hard gates prevent hallucinations
    - Output is always structured and explainable

    High-level flow:
        query
          → retrieve_context_with_scores
          → build RetrievalEvidence
          → score confidence (deterministic)
          → relevance gate (pre-LLM)
          → assemble_prompt
          → LLM.generate
          → answer-level gate (post-LLM)
          → RAGResult
    """

    # --- Basic input validation ---
    if not query or not query.strip():
        raise ValueError("Query must be a non-empty string")

    # ---------------------------------------------------------------------
    # 1. Retrieve context WITH similarity scores
    #    (scores are used internally only, never exposed to the LLM)
    # ---------------------------------------------------------------------
    retrieved = retrieve_context_with_scores(query, k=top_k)

    # ---------------------------------------------------------------------
    # 2. Build retrieval evidence objects (STEP 15)
    #    This creates a structured, explainable representation of retrieval
    # ---------------------------------------------------------------------
    evidence: list[RetrievalEvidence] = [
        RetrievalEvidence(
            chunk_id=f"chunk_{i}",
            source_document="unknown",  # placeholder until metadata pipeline
            similarity_score=score,
            chunk_text=text,
        )
        for i, (text, score) in enumerate(retrieved)
    ]

    # ---------------------------------------------------------------------
    # 3. Compute deterministic confidence BEFORE any LLM call
    #    This ensures confidence cannot be influenced by the model
    # ---------------------------------------------------------------------
    confidence = score_confidence(
        evidence=evidence,
        similarity_threshold=MIN_SIMILARITY_THRESHOLD,
    )

    # ---------------------------------------------------------------------
    # 4. Enforce grounding via relevance gate (hard stop, pre-LLM)
    #    If retrieval is weak, the LLM is never called
    # ---------------------------------------------------------------------
    if not is_context_relevant(retrieved):
        return RAGResult(
            query=query,
            answer=None,
            confidence=confidence,
            sources=[],
        )

    # ---------------------------------------------------------------------
    # 5. Prepare context for prompt assembly
    #    Strip all metadata — the LLM only sees clean text
    # ---------------------------------------------------------------------
    context_chunks: List[Dict] = [
        {"text": e.chunk_text}
        for e in evidence
    ]

    # ---------------------------------------------------------------------
    # 6. STEP 17 — Decide whether extractive-only mode is required
    #
    # Rationale:
    # - Small corpus + low evidence → higher hallucination risk
    # - Force extractive answers in these cases
    # ---------------------------------------------------------------------
    total_tokens = sum(len(c["text"].split()) for c in context_chunks)
    extractive_only = False

    if CORPUS_PROFILE == "small":
        if len(context_chunks) == 1 or total_tokens < 80:
            extractive_only = True

    # ---------------------------------------------------------------------
    # 7. Assemble the final prompt
    #    The LLM never sees confidence, similarity scores, or gating logic
    # ---------------------------------------------------------------------
    prompt = assemble_prompt(
        query=query,
        context_chunks=context_chunks,
        system_instruction=None,
        extractive_only=extractive_only,
    )

    # ---------------------------------------------------------------------
    # 8. Generate answer using the unified LLM interface
    # ---------------------------------------------------------------------
    llm = get_llm()
    answer = llm.generate(prompt)

    # ---------------------------------------------------------------------
    # 9. Enforce answer-level gate (STEP 20)
    #
    # This is a post-generation safety check.
    # Even with good retrieval, the answer itself may be unsafe.
    # ---------------------------------------------------------------------
    if not is_answer_allowed(
        answer=answer,
        confidence=confidence,
        extractive_only=extractive_only,
    ):
        return RAGResult(
            query=query,
            answer=None,
            confidence=confidence,
            sources=evidence,
        )

    # ---------------------------------------------------------------------
    # 10. Return structured, grounded, explainable result
    # ---------------------------------------------------------------------
    return RAGResult(
        query=query,
        answer=answer,
        confidence=confidence,
        sources=evidence,
    )
