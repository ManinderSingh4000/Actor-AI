
from models.scene import Scene
from models.schema import Script
from parsers.pdf_parser import parse_pdf
from fountain_parser import parse_fountain
from normalizer.normalize import normalize_script
from classifier.format_detector import detect_format

from normalizer.script_normalizer import normalize_script_to_canonical
from dataclasses import asdict
import json


def process_script(file_path: str) -> Script:
    format_type = detect_format(file_path)

    if format_type == "pdf":
        raw_text = parse_pdf(file_path)
        raw_text = normalize_script(raw_text)

        from parsers.pdf_parser import parse_pdf_lines
        return parse_pdf_lines(raw_text)

    elif format_type == "fountain":
        with open(file_path, "r", encoding="utf-8") as f:
            return parse_fountain(f.read())


if __name__ == "__main__":
    
    # ====================== For Fountain files ========================= #

    script = process_script("sample.fountain")
    canonical_scenes = normalize_script_to_canonical(script)

    with open("Fountain_Response/output_canonical.json", "w", encoding="utf-8") as f:
        json.dump(
            [scene.to_dict() for scene in canonical_scenes],
            f,
            indent=2,
            ensure_ascii=False
        )

print("✅ Script parsed successfully → output_canonical.json")

    # ====================== For PDF files ========================= #

#     script = process_script("test_script.pdf")   
#     canonical_scenes = normalize_script_to_canonical(script)

#     print(type(canonical_scenes[0]))


#     with open("PDF_Response/output_canonical.json", "w", encoding="utf-8") as f:
#         json.dump(
#             [scene.to_dict() for scene in canonical_scenes],
#             f,
#             indent=2,
#             ensure_ascii=False
#         )


# print("✅ Canonical script generated → output_canonical.json")

    