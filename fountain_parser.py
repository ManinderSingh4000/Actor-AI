import re
from models.schema import Scene, Dialogue, Script, Action, Parenthetical, uid

SCENE_RE = re.compile(r'^(INT|EXT)\.?\s', re.IGNORECASE)
CHAR_RE = re.compile(r'^([A-Z][A-Z0-9 ]{1,40})(?:\s*\(CONT[’\']?D\))?$')
PAREN_RE = re.compile(r'^\((.+)\)$')
BEAT_RE = re.compile(r'^(A beat\.|Beat\.|Pause\.)$', re.IGNORECASE)


def parse_fountain(text: str) -> Script:
    scenes = []
    current_scene = None
    current_character = None
    pending_parenthetical = None
    last_dialogue = None
    order = 1

    for raw in text.splitlines():
        line = raw.strip()

        # blank line → reset dialogue flow
        if not line:
            current_character = None
            pending_parenthetical = None
            last_dialogue = None
            continue

        # 🎬 Scene heading
        if SCENE_RE.match(line):
            current_scene = Scene(
                scene_id=uid("scene"),
                heading=line
            )
            scenes.append(current_scene)
            current_character = None
            continue

        if not current_scene:
            continue

        # 🗣 Character (handles CONT'D)
        m = CHAR_RE.match(line)
        if m:
            current_character = m.group(1)
            pending_parenthetical = None
            last_dialogue = None
            continue

        # 🎭 Parenthetical
        pm = PAREN_RE.match(line)
        if pm and current_character:
            raw_p = pm.group(1)
            emotions = [e.strip() for e in raw_p.split(",")]
            pending_parenthetical = Parenthetical(
                raw=raw_p,
                emotions=emotions
            )
            continue

        # 💬 Dialogue (merge wrapped lines)
        if current_character:
            if last_dialogue and last_dialogue.character == current_character:
                last_dialogue.text += " " + line
            else:
                d = Dialogue(
                    dialogue_id=uid("dlg"),
                    character=current_character,
                    text=line,
                    parenthetical=pending_parenthetical,
                    order=order
                )
                current_scene.dialogue.append(d)
                last_dialogue = d
                order += 1

            pending_parenthetical = None
            continue

        # 🎞 Action / Beat
        current_scene.action.append(
            Action(
                text=line,
                is_beat=bool(BEAT_RE.match(line))
            )
        )

    return Script(scenes=scenes)
