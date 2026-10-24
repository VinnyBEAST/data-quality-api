import pandas as pd

from app.qc import run_checks

GOOD_ROW = {
    "record_id": "R1",
    "name": "Amina",
    "district": "Gulu",
    "latitude": "2.77",
    "longitude": "32.30",
}


def make_df(*rows: dict) -> pd.DataFrame:
    return pd.DataFrame(rows, dtype=str)


def test_clean_file_has_no_issues():
    df = make_df(GOOD_ROW, {**GOOD_ROW, "record_id": "R2", "name": "Ben"})
    report = run_checks(df)
    assert report["rows"] == 2
    assert report["clean_rows"] == 2
    assert report["issues"] == []


def test_missing_column_stops_early():
    df = pd.DataFrame([{"record_id": "R1", "name": "Amina"}], dtype=str)
    report = run_checks(df)
    problems = {i["column"] for i in report["issues"]}
    assert {"district", "latitude", "longitude"} <= problems
    assert report["clean_rows"] == 0


def test_empty_required_field_is_flagged():
    df = make_df(GOOD_ROW, {**GOOD_ROW, "record_id": "R2", "district": "  "})
    report = run_checks(df)
    issue = report["issues"][0]
    assert issue["row"] == 3
    assert issue["column"] == "district"
    assert report["clean_rows"] == 1


def test_coordinate_out_of_range_is_flagged():
    df = make_df({**GOOD_ROW, "latitude": "95"})
    report = run_checks(df)
    assert report["issues"][0]["problem"] == "outside -90..90"
    assert report["clean_rows"] == 0


def test_non_numeric_coordinate_is_flagged():
    df = make_df({**GOOD_ROW, "longitude": "abc"})
    report = run_checks(df)
    assert report["issues"][0]["problem"] == "not a number"


def test_duplicate_record_id_keeps_first_occurrence():
    df = make_df(GOOD_ROW, {**GOOD_ROW, "name": "Copy"})
    report = run_checks(df)
    assert report["rows"] == 2
    assert report["clean_rows"] == 1
    dup = [i for i in report["issues"] if i["problem"] == "duplicate record_id"]
    assert len(dup) == 1 and dup[0]["row"] == 3


def test_row_with_several_problems_counted_once():
    df = make_df({**GOOD_ROW, "latitude": "95", "longitude": "400"})
    report = run_checks(df)
    assert len(report["issues"]) == 2
    assert report["clean_rows"] == 0
