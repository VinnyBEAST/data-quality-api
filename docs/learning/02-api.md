# Module 2: The API (`app/main.py`)

## FastAPI in one minute

FastAPI turns Python functions into web endpoints. The decorator tells it the
URL and HTTP method:

```python
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
```

FastAPI converts the returned dictionary to JSON. It also builds the
interactive page at `/docs` automatically from these functions and their type
hints.

## The two endpoints

| Method and URL | Purpose |
| --- | --- |
| `GET /health` | Returns `{"status": "ok"}`. Used by Docker and by monitoring to check the service is alive. |
| `POST /validate` | Accepts a CSV upload and returns the quality report. |

## Upload safety

The validate endpoint has three guards, in order:

1. **File type.** The name must end in `.csv`. Otherwise: HTTP 400.
2. **Size.** It reads at most 5 MB plus one byte. If the file is bigger, the
   read reveals it and the request gets HTTP 413 (too large). Reading only
   a fixed amount protects the server from very large uploads.
3. **Readable.** If pandas cannot parse the file, the request gets HTTP 400
   with the parser message.

## Why `dtype=str`

```python
df = pd.read_csv(io.BytesIO(content), dtype=str, keep_default_na=True)
```

Reading every column as text means pandas does not guess types. An ID like
`00123` keeps its leading zeros, and the checks decide what is valid. The
coordinate check converts to numbers itself.

## HTTP status codes to remember

| Code | Meaning in this project |
| --- | --- |
| 200 | Report returned |
| 400 | Bad input (wrong file type or unreadable CSV) |
| 413 | File too large |

## Check yourself

1. What does `async` and `await` do in the upload handler? (It lets the server
   handle other requests while it waits for the file to arrive.)
2. Why read only `MAX_UPLOAD_BYTES + 1` bytes?
3. Where can you see the API's documentation without writing any docs?

Previous: [Module 1](01-data-checks.md) · Next: [Module 3: Tests](03-tests.md)
