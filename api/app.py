from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uuid
import os
import tempfile

from main import process_script
from normalizer.script_normalizer import normalize_script_to_canonical


app = FastAPI(
    title="Screenplay Parsing API",
    version="1.0.0"
)

# ------------------------------------------------------------------
# In-memory temporary storage (SESSION SCOPE)
# ------------------------------------------------------------------

RAW_SCRIPTS = {}        # script_id -> { filename, path, format }
PARSED_SCRIPTS = {}    # script_id -> canonical scenes


def generate_script_id() -> str:
    return f"scr_{uuid.uuid4().hex[:16]}"


# ------------------------------------------------------------------
# 1️⃣ Root Endpoint
# ------------------------------------------------------------------

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Screenplay Parsing API. Use /docs for API documentation."
    }

# ------------------------------------------------------------------
# 1️⃣ Upload Endpoint
# ------------------------------------------------------------------

@app.post("/scripts/upload")
async def upload_script(file: UploadFile = File(...)):
    filename = file.filename.lower()

    if not (
        filename.endswith(".pdf")
        or filename.endswith(".fountain")
        or filename.endswith(".txt")
    ):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload PDF or Fountain."
        )

    script_id = generate_script_id()
    suffix = os.path.splitext(filename)[1]

    # Preserve extension for format detection
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    RAW_SCRIPTS[script_id] = {
        "filename": file.filename,
        "path": tmp_path,
        "format": "pdf" if suffix == ".pdf" else "fountain"
    }

    return {
        "status": "uploaded",
        "script_id": script_id,
        "format": RAW_SCRIPTS[script_id]["format"]
    }


# ------------------------------------------------------------------
# 2️⃣ Parse & Normalize Endpoint
# ------------------------------------------------------------------

@app.post("/scripts/{script_id}/parse")
def parse_script(script_id: str):
    if script_id not in RAW_SCRIPTS:
        raise HTTPException(
            status_code=404,
            detail="Script not found. Upload first."
        )

    if script_id in PARSED_SCRIPTS:
        return {
            "status": "already_parsed",
            "script_id": script_id,
            "scene_count": len(PARSED_SCRIPTS[script_id])
        }

    script_info = RAW_SCRIPTS[script_id]

    try:
        # Parse using existing pipeline
        script = process_script(script_info["path"])

        # Normalize to canonical blocks
        canonical_scenes = normalize_script_to_canonical(script)

        PARSED_SCRIPTS[script_id] = canonical_scenes

        return {
            "status": "parsed",
            "script_id": script_id,
            "scene_count": len(canonical_scenes)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ------------------------------------------------------------------
# 3️⃣ Fetch Structured Script
# ------------------------------------------------------------------

@app.get("/scripts/{script_id}/structure")
def get_script(script_id: str):
    if script_id not in PARSED_SCRIPTS:
        raise HTTPException(
            status_code=404,
            detail="Script not parsed yet."
        )

    scenes = PARSED_SCRIPTS[script_id]

    print("Response Generated...")

    return JSONResponse(
        content={
            "script_id": script_id,
            "scenes": [scene.to_dict() for scene in scenes]
        }
    )
