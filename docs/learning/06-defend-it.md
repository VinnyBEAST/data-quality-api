# Module 6: Defending the project

Practice answering these out loud. A good answer is short, names the file or
choice, and says why.

## Likely questions

**"What does your project do?"**
It checks survey CSV files for missing fields, bad coordinates and duplicate
IDs, and returns a JSON report. It runs as an API in a Docker container, and
GitHub Actions tests and builds it on every change.

**"Why FastAPI?"**
It is fast to write, generates the API documentation automatically, and uses
Python type hints to validate input.

**"Why pandas?"**
It reads CSV files and runs column-wise checks in a few lines, and it handles
missing values well.

**"How do you know it works?"**
Twelve automated tests cover the rules and the API. They run in CI on every
push, and the Docker image was built and its health check was tested.

**"What would you improve?"**
- Store reports in a database (for example Postgres) so results can be reviewed later.
- Add more rules, such as phone number format or district lists.
- Add authentication before real data is uploaded.
- Deploy to a host such as Render or Fly.io, which is not done yet.

**"Why does the duplicate rule keep the first record?"**
It is a simple, stated rule that is easy to explain. It can be changed in one
line if the business needs the latest record instead.

**"Why is the Docker image non-root?"**
If the app is compromised, the attacker has fewer permissions inside the container.

**"Did you write this with AI help?"**
Be honest about how you used tools. Be ready to explain every file, since
the test is whether you can change it yourself.

## Demo script (2 minutes)

1. Show the README and the folder structure.
2. Open `app/qc.py` and explain one rule.
3. Run `pytest -q` and show the green result.
4. Open `/docs`, upload `samples/sample_records.csv`, and read the report.
5. Open the Actions tab on GitHub and show a passing run.

## Being ready to change the code

Try these exercises yourself. They build the skill you need to defend it.

1. Add a check that the `name` field is at least 2 characters long. Write a test first.
2. Change the duplicate rule to keep the last record. Watch which test fails.
3. Make the district list come from a file.

Previous: [Module 5](05-ci-cd.md) · Back to [Module 0](00-overview.md)
