# Module 3: Tests (`tests/`)

## Why test

A test is a small program that checks the code does what it should. Tests
let you change code later and know quickly if you broke something.

## Running them

```bash
pytest -q
```

`-q` means quiet output. The expected result is `12 passed`.

## Two kinds of test

- **Unit tests** (`tests/test_qc.py`) call one function with made-up data and
  check the result. They do not use the web server.
- **API tests** (`tests/test_api.py`) send real HTTP-style requests to the app
  with `TestClient` and check the status code and the JSON.

## Anatomy of a test

```python
def test_duplicate_record_id_keeps_first_occurrence():
    df = make_df(GOOD_ROW, {**GOOD_ROW, "name": "Copy"})   # arrange
    report = run_checks(df)                                  # act
    assert report["clean_rows"] == 1                          # assert
```

Arrange, act, assert. Most tests follow this pattern.

## What the tests cover

| Test | Protects against |
| --- | --- |
| clean file has no issues | false alarms |
| missing column | crashes on wrong files |
| empty field | blank required data passing through |
| coordinate out of range | impossible locations |
| non-numeric coordinate | text in number fields |
| duplicate ID | double-counted records |
| row with two problems | counting one row twice |
| wrong extension, oversized file | upload guards |

## Check yourself

1. If you change the duplicate rule to keep the last occurrence, which test
   fails, and why is that good?
2. Why do the unit tests not need the web server?
3. What would you add next? (For example: a test for a file with only a header row.)

Previous: [Module 2](02-api.md) · Next: [Module 4: Docker](04-docker.md)
