from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TTSRequest:
    request_id: int
    event_id: int
    character: str
    text: str
    voice_id: str
    pace: float
    intensity: float
    pre_pause: float
    post_pause: float
    emotions: List[str]
