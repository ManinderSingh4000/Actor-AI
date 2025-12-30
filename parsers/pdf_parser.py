import fitz  # PyMuPDF
import re
from models.schema import Script, Scene, Dialogue

SCENE_RE = re.compile(r'^(INT|EXT)\.?\s', re.IGNORECASE)
PAREN_RE = re.compile(r'^\(.+\)$')


# ACTION_LIKE_RE = (
#     "pause", "silence", "beat", "breath",
#     "crackles", "rings", "bang", "footsteps",
#     "stares", "nods", "rubs", "tightens",
#     "stands", "turns", "begins", "stops",
#     "cuts off", "fades", "straightens", "sits",
#     "whispers", "shouts", "yells", "laughs",
#     "smiles", "grins", "looks", "glares",
#     "watches", "listens", "sighs", "groans",
#     "trembles", "quivers", "chuckles", "snickers",
#     "murmurs", "gasps", "cries", "weeps",
#     "screams", "howls", "roars", "snaps","steps",
#     "bolts","emerges","appears","disappears","approaches","withdraws",
#     "swerves"
# )

# def looks_like_action(line: str) -> bool:
#     l = line.lower()
#     return (
#         any(word in l for word in ACTION_LIKE_RE)
#         and not l.endswith("?")
#     )


def sounds_like_dialogue(line: str) -> bool:
    """
    Does this line sound like something a human would say?
    """
    return (
        "?" in line
        or "'" in line               # contractions: don't, I'm, it's
        or line.lower().startswith((
            "i ", "we ", "you ", "he ", "she ", "they "
        ))
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
    order = 1

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        # 🎬 Scene heading
        if SCENE_RE.match(line):
            current_scene = Scene(heading=line)
            scenes.append(current_scene)
            current_character = None
            pending_parenthetical = None
            continue

        if not current_scene:
            continue

        # 🗣 Character cue (JOHN / JOHN (V.O.))
        if line.isupper() and len(line.split()) <= 4:
            current_character = line
            pending_parenthetical = None
            continue

        # 🎭 Parenthetical on its own line
        if PAREN_RE.match(line) and current_character:
            pending_parenthetical = line.strip("()")
            continue

        # 💬 Dialogue
        if current_character:

    # 1️⃣ Implicit parenthetical (beat)
            if is_short_beat(line):
                pending_parenthetical = line.rstrip(".")
                continue

            # 2️⃣ Spoken dialogue
            if sounds_like_dialogue(line):
                current_scene.dialogue.append(
                    Dialogue(
                        character=current_character,
                        text=line,
                        parenthetical=pending_parenthetical,
                        order=order
                    )
                )
                order += 1
                pending_parenthetical = None
                continue

            # 3️⃣ Otherwise → action interrupt
            current_scene.action.append(line)
            continue


    return Script(scenes=scenes)