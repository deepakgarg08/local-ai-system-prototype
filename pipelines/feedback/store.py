import json
from pathlib import Path
from .models import UserFeedback

FEEDBACK_PATH = Path("data/feedback/feedback.jsonl")

def store_feedback(feedback: UserFeedback) -> None:
    FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)

    with FEEDBACK_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(feedback.__dict__, default=str) + "\n")
