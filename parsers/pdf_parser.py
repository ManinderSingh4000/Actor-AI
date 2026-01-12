import fitz  # PyMuPDF
import re
from models.schema import Script, Scene, Dialogue , Action , Parenthetical , uid

SCENE_RE = re.compile(r'^(INT|EXT)\.?\s', re.IGNORECASE)
PAREN_RE = re.compile(r'^\(.+\)$')
CHAR_VO_RE = re.compile(
    r'^([A-Z][A-Z ]{1,40})\s*(?:\((V\.O\.|O\.S\.|CONT[’\']?D)\))?$'
)


def sounds_like_dialogue(line: str) -> bool:
    # Must NOT look like action
    if re.search(r'\b(tightens|walks|stands|sits|stops|looks|turns|moves)\b', line.lower()):
        return False

    # Likely spoken
    return (
        "?" in line
        or line.startswith(("\"", "'"))
        or re.match(r'^(I|We|You|He|She|They)\b', line)
    )


def is_short_beat(line: str) -> bool:
    """
    Short descriptive beats often used as parentheticals.
    """
    return (
        len(line) <= 40
        and line.endswith(".")
        and line[0].isupper()
        and line.count(" ") <= 6
    )


def split_dialogue_action(line: str):
    if ". A " in line:
        parts = line.split(". A ", 1)
        return parts[0] + ".", "A " + parts[1]
    return line, None



def parse_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = []

    for page in doc:
        text.append(page.get_text())

    return "\n".join(text)


def parse_pdf_lines(text: str) -> Script:
    scenes = []
    current_scene = None
    current_character = None
    pending_parenthetical = None
    last_dialogue = None
    order = 1

    for raw in text.splitlines():
        line = raw.strip()

        if not line:
            current_character = None
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
            pending_parenthetical = None
            continue

        if not current_scene:
            continue

        # 🗣 Character cue (MARY / MARY (V.O.))
        m = CHAR_VO_RE.match(line)
        if m:
            current_character = m.group(1).strip()
            tag = m.group(2)

            pending_parenthetical = (
                Parenthetical(raw=tag, emotions=[]) if tag else None
            )
            last_dialogue = None
            continue

        # 🎭 Explicit parenthetical line
        if PAREN_RE.match(line) and current_character:
            raw_p = line.strip("()")
            pending_parenthetical = Parenthetical(
                raw=raw_p,
                emotions=[e.strip() for e in raw_p.split(",")]
            )
            continue

        # 🔹 Split mixed dialogue/action (if any)
        dialogue_part, action_part = split_dialogue_action(line)

        # 💬 Dialogue ONLY if character exists AND it sounds spoken
        if current_character and sounds_like_dialogue(dialogue_part):
            d = Dialogue(
                dialogue_id=uid("dlg"),
                character=current_character,
                text=dialogue_part,
                parenthetical=pending_parenthetical,
                order=order
            )
            current_scene.dialogue.append(d)
            last_dialogue = d
            order += 1
            pending_parenthetical = None

            # trailing action (rare but valid)
            if action_part:
                current_scene.action.append(
                    Action(
                        text=action_part,
                        is_beat=is_short_beat(action_part),
                        character_ref=None
                    )
                )
            continue

        # 🎞 DEFAULT → ACTION
        current_scene.action.append(
            Action(
                text=line,
                is_beat=is_short_beat(line),
                character_ref=None
            )
        )

    return Script(scenes=scenes)

