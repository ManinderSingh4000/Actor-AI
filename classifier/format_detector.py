def detect_format(file_path: str) -> str:
    ext = file_path.lower().split(".")[-1]

    if ext == "pdf":
        return "pdf"
    if ext in ("fountain", "txt"):
        return "fountain"

    raise ValueError("Unsupported file format")
