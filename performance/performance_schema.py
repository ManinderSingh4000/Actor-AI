from dataclasses import dataclass
from typing import List


@dataclass
class PerformanceNote:
    event_id: int
    emotion: str
    intensity: float
    pace_modifier: float
    emphasis_words: List[str]
