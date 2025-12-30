from models.schema import Dialogue
import re

BEAT_RE = re.compile(
    r'^(beat|a beat|pause|a pause|silence|a breath|then)$',
    re.IGNORECASE
)

def parse_dialogue(block: str, order: int) -> Dialogue:
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    character = lines[0]

    parenthetical = None
    text_lines = []

    for line in lines[1:]:
        # Explicit parenthetical
        if line.startswith("(") and line.endswith(")"):
            parenthetical = line.strip("()")
            continue

        # Implicit parenthetical / beat
        if BEAT_RE.match(line.lower()) or len(line) < 35 and line.endswith("."):
            parenthetical = line
            continue

        text_lines.append(line)

    return Dialogue(
        character=character,
        text=" ".join(text_lines),
        parenthetical=parenthetical,
        order=order
    )
