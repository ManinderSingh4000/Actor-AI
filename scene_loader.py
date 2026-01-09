import json
from models import Scene, DialogueLine, ActionLine

def normalize_character(name: str) -> str:
    return name.strip().upper()

def load_scene(json_path: str) -> Scene:
    with open(json_path, "r") as f:
        data = json.load(f)

    scene_data = data["scenes"][0]

    dialogue = [
        DialogueLine(
            dialogue_id=d["dialogue_id"],
            character=normalize_character(d["character"]),
            text=d["text"],
            order=d["order"]
        )
        for d in scene_data["dialogue"]
    ]

    action = [
        ActionLine(
            text=a["text"],
            is_beat=a["is_beat"]
        )
        for a in scene_data["action"]
    ]

    return Scene(
        scene_id=scene_data["scene_id"],
        heading=scene_data["heading"],
        dialogue=sorted(dialogue, key=lambda x: x.order),
        action=action
    )
