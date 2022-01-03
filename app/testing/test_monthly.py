from fastapi.testclient import TestClient

from app.dependencies import fetch_data
from app.main import app
from app.testing.dependency import override_dependency

client = TestClient(app)


app.dependency_overrides[fetch_data] = override_dependency


def test_monthly_controller():
    resp = client.get("/monthly")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": [
            {
                "moth": "2020-03",
                "positive": 6,
                "recovered": 4,
                "deaths": 4,
                "active": 6,
            },
            {
                "moth": "2021-01",
                "positive": 6,
                "recovered": 4,
                "deaths": 4,
                "active": 6,
            },
            {
                "moth": "2022-01",
                "positive": 6,
                "recovered": 5,
                "deaths": 5,
                "active": 6,
            },
        ],
        "message": "success",
    }


def test_monthly_year_controller():
    resp = client.get("/monthly/2022")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": [
            {
                "moth": "2022-01",
                "positive": 6,
                "recovered": 5,
                "deaths": 5,
                "active": 6,
            },
        ],
        "message": "success",
    }


def test_monthly_year_month_controller():
    resp = client.get("/monthly/2020/03")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": {
            "moth": "2020-03",
            "positive": 6,
            "recovered": 4,
            "deaths": 4,
            "active": 6,
        },
        "message": "success",
    }
