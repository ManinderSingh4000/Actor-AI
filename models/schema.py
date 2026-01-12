from dataclasses import dataclass, field
from typing import List, Optional
import uuid


def uid(prefix: str):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


@dataclass
class Parenthetical:
    raw: str
    emotions: List[str] = field(default_factory=list)


@dataclass
class Dialogue:
    dialogue_id: str
    character: str
    text: str
    parenthetical: Optional[Parenthetical] = None
    order: int = 0

@dataclass
class Transition:
    text: str


@dataclass
class Action:
    text: str
    is_beat: bool = False
    character_ref: Optional[str] = None


@dataclass
class Scene:
    scene_id: str
    heading: str
    action: List[Action] = field(default_factory=list)
    dialogue: List[Dialogue] = field(default_factory=list)
    transitions: List[Transition] = field(default_factory=list)



@dataclass
class Script:
    scenes: List[Scene]
