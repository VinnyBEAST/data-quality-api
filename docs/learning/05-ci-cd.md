# Module 5: CI/CD (`.github/workflows/ci.yml`)

## What it is

CI (continuous integration) runs tests automatically on every change. CD
(continuous delivery) builds and publishes the result. GitHub Actions runs
these steps on GitHub's servers, so you do not have to remember to test.

## Triggers

```yaml
on:
  push:
    branches: [main]
  pull_request:
```

- Every **pull request** runs the tests, so broken code is caught before merging.
- Every **push to main** runs the tests and then builds the image.

## Two jobs

**`test`** runs on every push and pull request:
1. Download the code.
2. Set up Python 3.12.
3. Install `requirements-dev.txt`.
4. Run `pytest -q`. If any test fails, the job fails and the change is flagged.

**`docker`** runs only after `test` passes, and only on `main`:
1. Log in to GitHub Container Registry with the built-in `GITHUB_TOKEN`.
2. Build the image and push it as `ghcr.io/<owner>/<repo>:latest`.

`needs: test` means "wait for test". `if: github.ref == 'refs/heads/main'`
means "only on the main branch".

## Secrets

The workflow uses `secrets.GITHUB_TOKEN`. GitHub creates this automatically
for each run, so there is nothing to paste in. The project has no passwords or
API keys in its code.

## Check yourself

1. Why does the Docker job depend on the test job?
2. Why does a pull request not publish an image?
3. Where would you see a failed test on GitHub? (The Actions tab.)

Previous: [Module 4](04-docker.md) · Next: [Module 6: Defending the project](06-defend-it.md)
