from .models import ConfidenceReport, RetrievalEvidence


def build_explanation(
    confidence: ConfidenceReport,
    evidence: list[RetrievalEvidence],
) -> str:
    stats = confidence.retrieval_stats or {}

    # --- Explicit IDK explanation ---
    if confidence.confidence_level == "none":
        if stats.get("relevance_gate") == "FAILED":
            return (
                "No sufficiently relevant internal information was found. "
                "The retrieved documents did not meet the relevance threshold, "
                "so the system did not generate an answer."
            )

        return (
            "The system could not determine an answer with sufficient grounding "
            "and therefore did not generate a response."
        )

    # --- Answer explanations ---
    sources = {e.source_document for e in evidence}
    num_chunks = stats.get("num_chunks", len(evidence))
    max_similarity = stats.get("max_similarity")

    explanation = (
        f"Confidence level: {confidence.confidence_level.upper()}. "
        f"The answer is based on {num_chunks} retrieved text section(s) "
        f"from {len(sources)} internal document(s)."
    )

    if max_similarity is not None and max_similarity < 0.6:
        explanation += (
            " The retrieved content is only weakly related to the query."
        )

    explanation += " Please verify the result before using it operationally."

    return explanation
