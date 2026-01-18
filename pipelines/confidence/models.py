from dataclasses import dataclass
from typing import Literal

@dataclass
class RetrievalEvidence:
    chunk_id: str
    source_document: str
    similarity_score: float
    chunk_text: str

@dataclass
class ConfidenceReport:
    confidence_level: Literal["high", "medium", "low", "none"]
    rationale: list[str]
    retrieval_stats: dict
