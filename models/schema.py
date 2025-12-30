from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Dialogue:
    character: str
    text: str
    parenthetical: Optional[str] = None
    order: int = 0

@dataclass
class Scene:
    heading: str
    action: List[str] = field(default_factory=list)
    dialogue: List[Dialogue] = field(default_factory=list)

@dataclass
class Script:
    scenes: List[Scene]
