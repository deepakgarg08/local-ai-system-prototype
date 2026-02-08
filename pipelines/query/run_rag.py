# pipelines/query/run_rag.py

from typing import List, Dict
from dataclasses import dataclass

# --- Query normalization for spelling ---
from pipelines.query.normalize import normalize_query

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

# --- Telemetry ---
from telemetry.confidence_logger import emit_confidence_event

import uuid
from data.registry import CHUNKS, SECTIONS, DOCUMENTS, FILES



@dataclass
class RAGResult:
    """
    End-to-end RAG execution WITH grounding, confidence, and explainability.

    =========================
    TEXT-ONLY BY DESIGN
    =========================
    This pipeline operates exclusively on TEXT.

    - Inputs: human-written text queries
    - Corpus: text chunks only
    - Retrieval: text embeddings
    - Context: plain text
    - Output: generated text

    No images, audio, video, spreadsheets, or structured databases
    are processed or interpreted at any stage.

    =========================
    HUMAN-IN-THE-LOOP BOUNDARIES
    =========================

    HUMAN — BEFORE EXECUTION
    ------------------------
    - Formulates the query
    - Defines intent, scope, and precision
    - Bears responsibility for ambiguity in the question

    SYSTEM — AUTOMATED EXECUTION
    ----------------------------
    - Retrieval, ranking, confidence scoring, gating,
      prompt assembly, and generation are fully automated
    - No human intervention is possible inside this function

    HUMAN — AFTER EXECUTION
    -----------------------
    - Reviews the answer (if any)
    - Validates correctness against source documents
    - Decides whether to accept, refine, or discard the result
    - Retains full responsibility for decisions and actions

    =========================
    ARCHITECTURAL GUARANTEES
    =========================
    - Retrieval happens before any LLM call
    - Confidence is computed deterministically (pre-LLM)
    - LLM never sees similarity scores or confidence
    - Multiple hard gates prevent hallucinations
    - Output is always structured and explainable

    High-level flow:
        Human query (text)
          → retrieve_context_with_scores
          → build RetrievalEvidence
          → score confidence (deterministic)
          → relevance gate (pre-LLM)
          → assemble_prompt (text-only)
          → LLM.generate (text-only)
          → answer-level gate (post-LLM)
          → RAGResult
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

    answer: str | None = None
    llm_backend: str | None = None
    execution_status = "OK"
    query_id = str(uuid.uuid4())
    confidence = None
    evidence = []
    normalized_query = None

    # ---------------------------------------------------------------------
    # 1. Retrieve context WITH similarity scores
    #    (scores are used internally only, never exposed to the LLM)
    # ---------------------------------------------------------------------
    try:
        normalized_query = normalize_query(query)
        retrieved = retrieve_context_with_scores(normalized_query, k=top_k)
        print(f"Retrieved {len(retrieved)} chunks with scores: {retrieved}")
        # ---------------------------------------------------------------------
        # 2. Build retrieval evidence objects (STEP 15)
        #    This creates a structured, explainable representation of retrieval
        # ---------------------------------------------------------------------

        evidence: list[RetrievalEvidence] = []

        for item in retrieved:
            chunk = CHUNKS[item["chunk_id"]]
            section = SECTIONS[chunk["section_id"]]
            document = DOCUMENTS[chunk["document_id"]]
            file = FILES[document["file_id"]]

            evidence.append(
                RetrievalEvidence(
                    chunk_id=chunk["chunk_id"],
                    source_document=document["document_name"],
                    similarity_score=item["similarity"],
                    chunk_text=chunk["text"],
                    section_title=section["section_title"],
                    section_path=section["section_path"],
                    file_path=file["path"],
                )
            )
        
        print(document["document_name"], section["section_title"])


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
            confidence = ConfidenceReport(
                confidence_level=confidence.confidence_level if confidence else None,
                rationale=["Insufficient relevant context retrieved"],
                retrieval_stats={
                        "num_chunks": len(retrieved),
                        "max_similarity": max((item["similarity"] for item in retrieved), default=None),
                        "relevance_gate": "FAILED",
                    },
                )
            return RAGResult(

                query=query,
                answer=None,
                confidence=confidence,
                sources=[],
            )

        # ---------------------------------------------------------------------
        # 5. Prepare context for prompt assembly
        #    TEXT-ONLY GUARANTEE:
        #    All metadata is stripped. The LLM receives plain text only.
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
        llm_backend = llm.__class__.__name__
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
            answer = None
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
            sources=evidence
        )
    except Exception as e:
        # Log the exception (placeholder for actual logging)
        print(f"Error during RAG execution: {e}")
        execution_status = "ERROR"
        raise

    finally:
        emit_confidence_event({
            "event_type": "rag_outcome",
            "query_id": query_id,
            "query": query,
            "normalized_query": normalized_query,
            "confidence_level": confidence.confidence_level if confidence else None,
            "rationale": confidence.rationale if confidence else None,
            "answer_type": "IDK" if answer is None else "ANSWER",
            "retrieval_stats": {
                "top_k": top_k,
                "num_chunks": len(evidence) if "evidence" in locals() else 0,
                "min_similarity": min(
                    (e.similarity_score for e in evidence),
                    default=None,
                ) if "evidence" in locals() else None,
            },
            "model_backend": llm_backend,
            "execution_status": execution_status,

        })
