
from models.schema import Script
from parsers.pdf_parser import parse_pdf
from fountain_parser import parse_fountain
from normalizer.normalize import normalize_script

from classifier.format_detector import detect_format

def process_script(file_path: str) -> Script:
    format_type = detect_format(file_path)

    if format_type == "pdf":
        raw_text = parse_pdf(file_path)
        raw_text = normalize_script(raw_text)
        from parsers.pdf_parser import parse_pdf_lines
        return parse_pdf_lines(raw_text)
        

    elif format_type == "fountain":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # text = normalize_unicode(text)
        return parse_fountain(text)

if __name__ == "__main__":
    
    # ====================== For Fountain files ========================= #

    # script = process_script("sample.fountain")

    # with open("Fountain_Response/output415.json", "w", encoding="utf-8") as f:
    #     import json
    #     from dataclasses import asdict
    #     json.dump(asdict(script), f, indent=2, ensure_ascii=False)

    # print("✅ Script parsed successfully → output415.json")

    # ====================== For PDF files ========================= #

    script = process_script("paren.pdf")   
    with open("PDF_Response/output_updated_01.json", "w", encoding="utf-8") as f:
        import json     
        from dataclasses import asdict
        json.dump(asdict(script), f, indent=2, ensure_ascii=False)  
    print("✅ Script parsed successfully → output_updated.json")

    