import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


LOG_DIR = Path("logs/confidence/runtime")


def emit_confidence_projection(rag_event: Dict[str, Any]) -> None:
    """
    Create a simplified confidence analytics record
    derived from canonical rag_event.
    Never mutates original.
    Never raises.
    """

    try:
        # Do not log during tests
        if os.environ.get("PYTEST_CURRENT_TEST"):
            return

        LOG_DIR.mkdir(parents=True, exist_ok=True)

        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_file = LOG_DIR / f"{date}.jsonl"

        projection = {
            "event_id": rag_event.get("event_id"),
            "timestamp": rag_event.get("timestamp"),
            "query": rag_event["query"]["raw"],
            "normalized_query": rag_event["query"]["normalized"],
            "confidence_level": rag_event["confidence"]["level"],
            "confidence_score": rag_event["confidence"]["score"],
            "confidence_method": rag_event["confidence"]["method"],
            "answer_type": rag_event["result"]["answer_type"],
            "gate_passed": rag_event["relevance_gate"]["passed"],
            "max_similarity": rag_event["retrieval"]["max_similarity"],
        }

        with log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(projection, ensure_ascii=False) + "\n")

    except Exception:
        pass
