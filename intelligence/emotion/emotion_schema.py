from dataclasses import dataclass
from typing import List


@dataclass
class EmotionNote:
    event_id: int
    emotions: List[str]
    confidence: float
