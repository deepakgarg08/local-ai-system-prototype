# pipelines/confidence/models.py

from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class RetrievalEvidence:
    chunk_id: str
    source_document: str
    similarity_score: float
    chunk_text: str
    # NEW (STEP 29 – provenance)
    section_title: Optional[str] = None
    section_path: Optional[str] = None
    file_path: Optional[str] = None

@dataclass
class ConfidenceReport:
    confidence_level: Literal["high", "medium", "low", "none"]
    rationale: list[str]
    retrieval_stats: dict
