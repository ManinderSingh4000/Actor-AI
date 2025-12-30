import re
from models.schema import Scene, Dialogue, Script

SCENE_RE = re.compile(r'^(INT|EXT)\.?\s', re.IGNORECASE)
CHAR_RE = re.compile(r'^[A-Z][A-Z0-9 ()\.]{1,40}$')
PAREN_RE = re.compile(r'^\(.+\)$')

def parse_fountain(text: str) -> Script:
    scenes = []
    current_scene = None
    current_character = None
    pending_parenthetical = None
    order = 1

    lines = text.splitlines()

    for raw in lines:
        line = raw.rstrip()

        # 🔹 Blank line → reset dialogue flow
        if not line.strip():
            current_character = None
            pending_parenthetical = None
            continue

        # 🎬 Scene Heading
        if SCENE_RE.match(line):
            current_scene = Scene(heading=line.strip())
            scenes.append(current_scene)
            current_character = None
            pending_parenthetical = None
            continue

        if not current_scene:
            continue

        # 🗣 Character
        if CHAR_RE.match(line.strip()):
            current_character = line.strip()
            pending_parenthetical = None
            continue

        # 🎭 Parenthetical
        if PAREN_RE.match(line.strip()) and current_character:
            pending_parenthetical = line.strip("()")
            continue

        # 💬 Dialogue
        if current_character:
            current_scene.dialogue.append(
                Dialogue(
                    character=current_character,
                    text=line.strip(),
                    parenthetical=pending_parenthetical,
                    order=order
                )
            )
            order += 1
            pending_parenthetical = None
            continue

        # 🎞 Action
        current_scene.action.append(line.strip())

    return Script(scenes=scenes)


# with open("sample.fountain") as f:
#     text = f.read()

# script = parse_fountain(text)

# import json
# from dataclasses import asdict
# print(json.dumps(asdict(script), indent=2))

# with open("output_fountain.json", "w") as f:
#     json.dump(asdict(script), f, indent=2)
