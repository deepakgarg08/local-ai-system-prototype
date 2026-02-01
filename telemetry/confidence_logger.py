import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


LOG_DIR = Path("logs/confidence/runtime")


def emit_confidence_event(event: Dict[str, Any]) -> None:
    """
    Append one confidence telemetry event as JSONL.
    Must never raise.
    Runtime telemetry ONLY (never during tests).
    """
    try:
        # ⛔ Do NOT emit telemetry during pytest
        if os.environ.get("PYTEST_CURRENT_TEST"):
            return

        LOG_DIR.mkdir(parents=True, exist_ok=True)

        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_file = LOG_DIR / f"{date}.jsonl"

        # ⚠️ Do NOT mutate the original event dict
        payload = dict(event)
        payload["logged_at"] = datetime.now(timezone.utc).isoformat()

        with log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    except Exception:
        # Telemetry must NEVER break the main flow
        pass
