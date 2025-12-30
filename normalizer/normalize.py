


import re

def normalize_script(text: str) -> str:
    text = text.replace("\r", "")

    # Remove ZERO WIDTH + BOM chars ONLY
    text = re.sub(r'[\u200b\u200c\u200d\uFEFF]', '', text)
    text = text.replace("\u2026", "...")
    text = text.replace("\u2014", "--")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2019", "'")



    # Normalize scene headings
     # Ensure scene headings start on their own block
    text = re.sub(r'\n?(INT|EXT)\.?\s+', r'\n\n\1. ', text)

    # Collapse excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Collapse excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Normalize VO / OS markers
    text = re.sub(r'\(\s*V\.O\.\s*\)', '(V.O.)', text, flags=re.IGNORECASE)
    text = re.sub(r'\(\s*O\.S\.\s*\)', '(O.S.)', text, flags=re.IGNORECASE)
    text = re.sub(r'\(\s*CONT[’\']?D\s*\)', '(CONT’D)', text, flags=re.IGNORECASE)


    return text.strip()
