from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class TimelineEvent:
    event_id: int
    type: str  # dialogue | beat | action | transition
    scene_id: str
    character: Optional[str]
    text: Optional[str]
    estimated_duration: float
    metadata: Dict[str, Any]

