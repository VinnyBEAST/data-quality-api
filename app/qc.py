"""Quality checks for survey-style CSV records.

The rules here are deliberately simple and explicit so each issue can be
explained to a reviewer: missing columns, empty required fields, coordinates
outside valid ranges, and duplicate record IDs.
"""

from dataclasses import dataclass, asdict

import pandas as pd

REQUIRED_COLUMNS = ["record_id", "name", "district", "latitude", "longitude"]


@dataclass
class Issue:
    row: int | None
    column: str | None
    problem: str

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    """Make headers match the required names: "Record ID " becomes "record_id"."""
    df = df.copy()
    df.columns = [
        str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns
    ]
    return df


def check_columns(df: pd.DataFrame) -> list[Issue]:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return [Issue(None, c, "missing required column") for c in missing]


def check_required_fields(df: pd.DataFrame) -> list[Issue]:
    issues = []
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            continue
        empty = df[column].isna() | (df[column].astype(str).str.strip() == "")
        for idx in df.index[empty]:
            issues.append(Issue(int(idx) + 2, column, "empty required field"))
    return issues


def check_coordinates(df: pd.DataFrame) -> list[Issue]:
    issues = []
    if "latitude" not in df.columns or "longitude" not in df.columns:
        return issues
    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    for idx in df.index[lat.isna() & df["latitude"].notna()]:
        issues.append(Issue(int(idx) + 2, "latitude", "not a number"))
    for idx in df.index[lon.isna() & df["longitude"].notna()]:
        issues.append(Issue(int(idx) + 2, "longitude", "not a number"))
    for idx in df.index[(lat < -90) | (lat > 90)]:
        issues.append(Issue(int(idx) + 2, "latitude", "outside -90..90"))
    for idx in df.index[(lon < -180) | (lon > 180)]:
        issues.append(Issue(int(idx) + 2, "longitude", "outside -180..180"))
    return issues


def find_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, list[Issue]]:
    """Keep the first occurrence of each record_id and report the rest."""
    if "record_id" not in df.columns:
        return df, []
    dup_mask = df.duplicated(subset="record_id", keep="first")
    issues = [
        Issue(int(idx) + 2, "record_id", "duplicate record_id")
        for idx in df.index[dup_mask]
    ]
    return df[~dup_mask].copy(), issues


def run_checks(df: pd.DataFrame) -> dict:
    """Run every check and return a report with counts and issues."""
    column_issues = check_columns(df)
    if column_issues:
        return {
            "rows": len(df),
            "clean_rows": 0,
            "issues": [i.to_dict() for i in column_issues],
        }

    issues = check_required_fields(df) + check_coordinates(df)
    deduped, dup_issues = find_duplicates(df)
    issues += dup_issues

    # A row is clean only if no issue points at it.
    bad_rows = {i.row for i in issues if i.row is not None}
    clean_rows = len(deduped) - sum(1 for r in bad_rows if r - 2 in deduped.index)

    return {
        "rows": len(df),
        "clean_rows": clean_rows,
        "issues": [i.to_dict() for i in issues],
    }
