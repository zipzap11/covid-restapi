from fastapi.testclient import TestClient

from app.dependencies import fetch_data
from app.main import app
from app.testing.dependency import override_dependency

client = TestClient(app)

app.dependency_overrides = {}
app.dependency_overrides[fetch_data] = override_dependency


def test_general_controller():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": True,
        "data": {
            "total_positive": 18,
            "total_recovered": 13,
            "total_deaths": 13,
            "total_active": 18,
            "new_positive": 13,
            "new_recovered": 1,
            "new_deaths": 5,
            "new_active": 6,
        },
        "message": "success",
    }
