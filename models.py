from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class DialogueLine:
    dialogue_id: str
    character: str
    text: str
    order: int

@dataclass
class ActionLine:
    text: str
    is_beat: bool

@dataclass
class Scene:
    scene_id: str
    heading: str
    dialogue: List[DialogueLine]
    action: List[ActionLine]

@dataclass
class SceneAssignment:
    ai_character: str
    user_character: str

@dataclass
class SceneAssets:
    ai_audio_map: Dict[str, str]  # dialogue_id → wav path
