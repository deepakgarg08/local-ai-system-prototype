import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


LOG_DIR = Path("logs/confidence")


def emit_confidence_event(event: Dict[str, Any]) -> None:
    """
    Append one confidence telemetry event as JSONL.
    Must never raise.
    """
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_file = LOG_DIR / f"{date}.jsonl"

        event["logged_at"] = datetime.now(timezone.utc).isoformat()

        with log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    except Exception:
        # Telemetry must NEVER break the main flow
        pass
