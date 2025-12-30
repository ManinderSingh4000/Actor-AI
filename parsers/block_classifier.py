
import re

def classify_block(block: str) -> str:
    lines = block.split("\n")
    first = lines[0].strip()

    # Normalize spacing
    normalized = re.sub(r"\s+", " ", first)

    # Scene Heading (robust)
    if re.match(r"^(INT|EXT)\.?\s", normalized):
        return "SCENE"

    # Dialogue
    if (
        first.isupper()
        and len(first.split()) <= 4
        and len(lines) >= 2
    ):
        return "DIALOGUE"

    # Transition
    if first.isupper() and first.endswith("TO:"):
        return "TRANSITION"

    return "ACTION"
