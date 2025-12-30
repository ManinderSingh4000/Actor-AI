from dataclasses import dataclass
from typing import List


@dataclass
class NarrativeInsight:
    scene_id: str
    tension_curve: List[float]
    pacing: str
    dominant_emotions: List[str]
