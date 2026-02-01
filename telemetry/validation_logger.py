import json
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs/confidence/validation")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "validation_events.jsonl"


def emit_validation_event(
    stage: str,
    status: str,
    details: dict | None = None,
):
    event = {
        "event_type": "validation",
        "stage": stage,                # e.g. "confidence_threshold_calibration"
        "status": status,              # PASS / FAIL
        "details": details or {},
        "logged_at": datetime.utcnow().isoformat() + "Z",
    }

    with LOG_FILE.open("a") as f:
        f.write(json.dumps(event) + "\n")
