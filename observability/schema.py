# observability/schema.py

from dataclasses import dataclass
from typing import Optional, Dict, Any
import uuid
from datetime import datetime, timezone


def build_rag_event(
    *,
    raw_query: str,
    normalized_query: str,
    user_role: str,
    session_id: Optional[str],
    retrieval_stats: Dict[str, Any],
    relevance_gate: Dict[str, Any],
    llm_stats: Dict[str, Any],
    confidence: Dict[str, Any],
    result: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": {
            "raw": raw_query,
            "normalized": normalized_query,
            "user_role": user_role,
            "session_id": session_id,
        },
        "retrieval": retrieval_stats,
        "relevance_gate": relevance_gate,
        "llm": llm_stats,
        "confidence": confidence,
        "result": result,
    }
