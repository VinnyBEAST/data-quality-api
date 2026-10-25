from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

GOOD_CSV = (
    "record_id,name,district,latitude,longitude\n"
    "R1,Amina,Gulu,2.77,32.30\n"
    "R2,Ben,Mbale,1.08,34.18\n"
)


def upload(content: bytes, filename: str = "records.csv"):
    return client.post("/validate", files={"file": (filename, content, "text/csv")})


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_valid_csv_returns_clean_report():
    response = upload(GOOD_CSV.encode())
    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "records.csv"
    assert body["rows"] == 2
    assert body["clean_rows"] == 2
    assert body["issues"] == []


def test_csv_with_problems_is_reported():
    bad = GOOD_CSV + "R1,Dup,Gulu,99,32\n"
    body = upload(bad.encode()).json()
    assert body["rows"] == 3
    problems = {i["problem"] for i in body["issues"]}
    assert "duplicate record_id" in problems
    assert "outside -90..90" in problems


def test_non_csv_extension_is_rejected():
    response = upload(GOOD_CSV.encode(), filename="records.txt")
    assert response.status_code == 400


def test_oversized_file_is_rejected():
    response = upload(b"x" * (5 * 1024 * 1024 + 10))
    assert response.status_code == 413


def test_headers_with_spaces_and_case_are_accepted():
    csv = (
        "Record ID,Name,District,Latitude,Longitude\n"
        "R1,Amina,Gulu,2.77,32.30\n"
    )
    body = upload(csv.encode()).json()
    assert body["issues"] == []
    assert body["clean_rows"] == 1


def test_excel_byte_order_mark_is_handled():
    csv = "﻿record_id,name,district,latitude,longitude\nR1,Amina,Gulu,2.77,32.30\n"
    body = upload(csv.encode("utf-8")).json()
    assert body["issues"] == []


def test_missing_column_is_reported_not_crashed():
    csv = "record_id,name,district\nR1,Amina,Gulu\n"
    response = upload(csv.encode())
    assert response.status_code == 200
    problems = {i["column"] for i in response.json()["issues"]}
    assert {"latitude", "longitude"} <= problems


def test_non_utf8_file_gets_clear_error():
    response = upload("name\nJosé\n".encode("latin-1") + b"\xff\xfe")
    assert response.status_code == 400
    assert "UTF-8" in response.json()["detail"]


def test_empty_file_gets_clear_error():
    response = upload(b"")
    assert response.status_code == 400


def test_upload_page_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "Data Quality Checker" in response.text
    assert 'id="file"' in response.text
