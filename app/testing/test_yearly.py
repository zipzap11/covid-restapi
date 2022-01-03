from fastapi.testclient import TestClient

from app.dependencies import fetch_data
from app.main import app
from app.testing.dependency import override_dependency

client = TestClient(app)


app.dependency_overrides[fetch_data] = override_dependency


def test_yearly_controller():
    resp = client.get("/yearly")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": [
            {
                "year": 2020,
                "positive": 6,
                "recovered": 4,
                "deaths": 4,
                "active": 6,
            },
            {
                "year": 2021,
                "positive": 6,
                "recovered": 4,
                "deaths": 4,
                "active": 6,
            },
            {
                "year": 2022,
                "positive": 6,
                "recovered": 5,
                "deaths": 5,
                "active": 6,
            },
        ],
        "message": "success",
    }


def test_yearly_year_controller():
    resp = client.get("/yearly/2020")

    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": {
            "year": "2020",
            "positive": 6,
            "recovered": 4,
            "deaths": 4,
            "active": 6,
        },
        "message": "success",
    }
