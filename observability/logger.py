# observability/logger.py

import json
from pathlib import Path
from typing import Dict, Any

LOG_PATH = Path("logs/rag_events.jsonl")


def log_event(layer: str, event: Dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    event_with_layer = {**event, "layer": layer}

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event_with_layer) + "\n")
