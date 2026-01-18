from .models import RetrievalEvidence, ConfidenceReport

def score_confidence(
    evidence: list[RetrievalEvidence],
    similarity_threshold: float
) -> ConfidenceReport:
    if not evidence:
        return ConfidenceReport(
            confidence_level="none",
            rationale=["No relevant context retrieved"],
            retrieval_stats={}
        )

    scores = [e.similarity_score for e in evidence]
    documents = {e.source_document for e in evidence}

    rationale = []
    retrieval_stats = {
        "num_chunks": len(evidence),
        "num_documents": len(documents),
        "min_score": min(scores),
        "max_score": max(scores),
    }

    if len(evidence) >= 3 and len(documents) >= 2 and min(scores) >= similarity_threshold:
        rationale.append("Multiple high-similarity chunks from different documents")
        level = "high"
    elif len(evidence) >= 2:
        rationale.append("Limited but relevant context found")
        level = "medium"
    else:
        rationale.append("Only weak or single-context match found")
        level = "low"

    return ConfidenceReport(
        confidence_level=level,
        rationale=rationale,
        retrieval_stats=retrieval_stats
    )
