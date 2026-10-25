# Module 1: The data checks (`app/qc.py`)

## The required columns

```python
REQUIRED_COLUMNS = ["record_id", "name", "district", "latitude", "longitude"]
```

Every record must have these five columns. Changing this list changes what
the service expects.

## The `Issue` record

```python
@dataclass
class Issue:
    row: int | None
    column: str | None
    problem: str
```

Each problem is stored as an `Issue`. `row` is the spreadsheet row number, so
row 1 is the header and the first data row is row 2. That is why the code
writes `int(idx) + 2`: pandas counts from 0 and the header takes row 1.

## The four checks

| Function | What it catches |
| --- | --- |
| `check_columns` | A required column is missing from the file |
| `check_required_fields` | A required cell is empty or only spaces |
| `check_coordinates` | Latitude or longitude is not a number, or is out of range |
| `find_duplicates` | A `record_id` appears more than once |

### Empty fields

```python
empty = df[column].isna() | (df[column].astype(str).str.strip() == "")
```

`isna()` catches truly blank cells. The second part catches cells that contain
only spaces. The `|` means "or".

### Coordinates

Latitude must be between -90 and 90, and longitude between -180 and 180.
The code first converts the text to numbers with `pd.to_numeric(..., errors="coerce")`.
Values that cannot be read as numbers become `NaN`, which lets us report them
as "not a number".

### Duplicates

```python
dup_mask = df.duplicated(subset="record_id", keep="first")
```

The first occurrence of an ID is kept, and every later one is reported and
removed. This is a deliberate rule. If you ever need a different one, such as
keeping the most recent record, change this line.

## Building the report

`run_checks` runs everything and counts clean rows. A row with two problems
is counted once, because the code collects the bad row numbers in a set.

```python
bad_rows = {i.row for i in issues if i.row is not None}
```

A set removes duplicates automatically, so a row with two problems counts once.

## Check yourself

1. Why does the code add 2 to the row index?
2. What is the difference between `isna()` and `== ""`?
3. A row has a bad latitude, and its `record_id` also appears earlier in the file. How many clean rows do you lose, and why?
   (Answer: the row is excluded either way, but it is counted once, not twice, because the bad row numbers are collected in a set.)
4. Where would you add a new rule, such as checking phone numbers?

Previous: [Module 0](00-overview.md) · Next: [Module 2: The API](02-api.md)
