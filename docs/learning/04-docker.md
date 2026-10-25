# Module 4: Docker (`Dockerfile`, `docker-compose.yml`)

## The problem Docker solves

"It works on my machine" fails when the app moves to another computer. Docker
packages the app together with its exact Python version and libraries, so it
runs the same way everywhere.

## The Dockerfile, line by line

| Line | What it does |
| --- | --- |
| `FROM python:3.12-slim` | Start from an official small Python 3.12 image |
| `WORKDIR /app` | Work inside `/app` in the container |
| `COPY requirements.txt .` then `RUN pip install` | Install libraries. Copying this file first lets Docker cache the install step, so rebuilds are faster when only code changes. |
| `COPY app ./app` | Copy the application code |
| `RUN useradd ... USER appuser` | Run as a non-root user, so a hacked process has fewer rights |
| `EXPOSE 8000` | Document the port the app listens on |
| `HEALTHCHECK` | Docker calls `/health` and marks the container unhealthy if it fails |
| `CMD [...]` | The command that starts the server |

## Why the tests are not in the image

`.dockerignore` excludes `tests/` and the virtual environment. The image only
needs what runs the service, which keeps it smaller and more secure.

## Running it

```bash
docker compose up --build
```

`up` starts the container. `--build` rebuilds the image first. The API is then
at http://localhost:8000.

## Check yourself

1. Why do we copy `requirements.txt` before copying the code?
2. Why does the container run as `appuser` and not as root?
3. What would happen if `.dockerignore` did not exclude `.venv/`?

Previous: [Module 3](03-tests.md) · Next: [Module 5: CI/CD](05-ci-cd.md)
