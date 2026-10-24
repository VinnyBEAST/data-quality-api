import io

import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile

from app.qc import run_checks

MAX_UPLOAD_BYTES = 5 * 1024 * 1024

app = FastAPI(
    title="Data Quality API",
    description="Upload a CSV of survey records and get a quality report.",
    version="0.1.0",
)


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
        df = pd.read_csv(io.BytesIO(content), dtype=str, keep_default_na=True)
    except (pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {exc}")

    return {"filename": file.filename, **run_checks(df)}
