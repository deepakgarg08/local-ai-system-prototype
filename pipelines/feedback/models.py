from dataclasses import dataclass
from typing import Literal
from datetime import datetime


@dataclass
class UserFeedback:
    query: str
    answer: str | None
    confidence_level: str
    user_rating: Literal["correct", "partially_correct", "incorrect"]
    comment: str | None
    timestamp: datetime
