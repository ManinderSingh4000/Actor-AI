from dataclasses import dataclass, field
from typing import List


@dataclass
class CharacterProfile:
    character_id: str
    scenes_present: List[str] = field(default_factory=list)
    dialogue_count: int = 0
    action_mentions: int = 0
    delivery_modes: List[str] = field(default_factory=list)
    first_event_id: int = 0
    last_event_id: int = 0
