from fastapi.testclient import TestClient

from app.dependencies import fetch_data
from app.main import app
from app.testing.dependency import override_dependency

client = TestClient(app)


app.dependency_overrides[fetch_data] = override_dependency


def test_monthly_controller():
    resp = client.get("/daily")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": [
            {
                "date": "2020-03-02",
                "positive": 2,
                "recovered": 1,
                "deaths": 1,
                "active": 2,
            },
            {
                "date": "2020-03-03",
                "positive": 4,
                "recovered": 3,
                "deaths": 3,
                "active": 4,
            },
            {
                "date": "2021-01-01",
                "positive": 2,
                "recovered": 1,
                "deaths": 1,
                "active": 2,
            },
            {
                "date": "2021-01-02",
                "positive": 4,
                "recovered": 3,
                "deaths": 3,
                "active": 4,
            },
            {
                "date": "2022-01-02",
                "positive": 6,
                "recovered": 5,
                "deaths": 5,
                "active": 6,
            },
        ],
        "message": "success",
    }


def test_daily_year_controller():
    resp = client.get("/daily/2022")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": [
            {
                "date": "2022-01-02",
                "positive": 6,
                "recovered": 5,
                "deaths": 5,
                "active": 6,
            },
        ],
        "message": "success",
    }


def test_daily_year_month_controller():
    resp = client.get("/daily/2022/01")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": [
            {
                "date": "2022-01-02",
                "positive": 6,
                "recovered": 5,
                "deaths": 5,
                "active": 6,
            },
        ],
        "message": "success",
    }


def test_daily_year_month_day_controller():
    resp = client.get("/daily/2022/01/02")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": {
            "date": "2022-01-02",
            "positive": 6,
            "recovered": 5,
            "deaths": 5,
            "active": 6,
        },
        "message": "success",
    }
