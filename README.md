# Data Quality API

A small FastAPI service that checks survey-style CSV files for common problems
and returns a JSON report.

It checks for:
- missing required columns (`record_id`, `name`, `district`, `latitude`, `longitude`)
- empty required fields
- non-numeric or out-of-range coordinates
- duplicate `record_id` values (the first occurrence is kept)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs to try the `/validate` endpoint.

## Run with Docker

```bash
docker compose up --build
```

## Example

```bash
curl -F "file=@records.csv" http://localhost:8000/validate
```

```json
{
  "filename": "records.csv",
  "rows": 3,
  "clean_rows": 2,
  "issues": [
    {"row": 4, "column": "record_id", "problem": "duplicate record_id"}
  ]
}
```

Row numbers match the spreadsheet: row 1 is the header, so the first data row is row 2.

## Tests

```bash
pytest -q
```

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`):
- runs the test suite on every push and pull request
- on pushes to `main`, builds the Docker image and pushes it to GitHub Container Registry

## Design notes

- Rules are plain functions in `app/qc.py`, so each one is easy to read and test.
- Uploads are limited to 5 MB and must be `.csv`.
- All data in this repo is synthetic.
