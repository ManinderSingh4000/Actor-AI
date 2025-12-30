def split_into_blocks(text: str) -> list[str]:
    blocks = []
    current = []

    for line in text.splitlines():
        line = line.rstrip()

        if line == "":
            if current:
                blocks.append("\n".join(current))
                current = []
        else:
            current.append(line)

    if current:
        blocks.append("\n".join(current))

    return blocks
