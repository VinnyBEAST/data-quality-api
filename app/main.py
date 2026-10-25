import io
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.qc import normalize_headers, run_checks

MAX_UPLOAD_BYTES = 5 * 1024 * 1024
PAGE = Path(__file__).parent / "static" / "index.html"

app = FastAPI(
    title="Data Quality API",
    description="Upload a CSV of survey records and get a quality report.",
    version="0.1.0",
)


@app.get("/", include_in_schema=False)
def upload_page() -> FileResponse:
    return FileResponse(PAGE)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/validate")
async def validate(file: UploadFile) -> dict:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a .csv file")

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File is larger than 5 MB")

    try:
        # utf-8-sig also handles files saved by Excel, which add a hidden byte-order mark.
        df = pd.read_csv(io.BytesIO(content), dtype=str, encoding="utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {exc}")

    return {"filename": file.filename, **run_checks(normalize_headers(df))}
