# Module 0: Overview

## What the project does

A user uploads a CSV file of survey records. The service checks every row and
returns a JSON report that says how many rows are clean and which rows have
problems, and why.

```
 CSV upload ──► POST /validate ──► pandas DataFrame ──► run_checks() ──► JSON report
                 (app/main.py)                          (app/qc.py)
```

## Why it is built this way

- **Small and explicit.** Each rule is a plain function. A reviewer can read
  the whole checking logic in one file.
- **Testable.** The rules do not depend on the web server, so they can be
  tested directly.
- **Deployable.** It runs in a container and is tested and built by GitHub
  Actions on every push.

## The files

| File | Job |
| --- | --- |
| `app/qc.py` | The data checks (the core logic) |
| `app/main.py` | The web API that accepts uploads |
| `tests/test_qc.py` | Tests for the checks |
| `tests/test_api.py` | Tests for the API |
| `Dockerfile` | Recipe for the container image |
| `docker-compose.yml` | Runs the container with one command |
| `.github/workflows/ci.yml` | Automated tests and image build |
| `requirements.txt` | Libraries the app needs to run |
| `requirements-dev.txt` | Extra libraries for testing |
| `samples/sample_records.csv` | Example data with known problems |

## Words you will hear

- **API**: a way for programs to talk to the service over HTTP.
- **Endpoint**: one URL the API serves, such as `/validate`.
- **DataFrame**: a table in memory, from the pandas library.
- **Container**: a packaged app with everything it needs to run anywhere.
- **CI/CD**: automation that tests (CI) and ships (CD) code on each change.

## Check yourself

1. What does the user send, and what do they get back?
2. Which file contains the business rules?
3. Why are the rules kept separate from the web code?

Next: [Module 1: The data checks](01-data-checks.md)
