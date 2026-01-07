from fastapi.testclient import TestClient

from app.main import DEFAULT_MAX, DEFAULT_MIN, app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_random_default_range():
    response = client.get("/random")
    assert response.status_code == 200
    body = response.json()
    assert DEFAULT_MIN <= body["number"] <= DEFAULT_MAX


def test_random_custom_range():
    lower, upper = 5, 10
    response = client.get(f"/random?min_value={lower}&max_value={upper}")
    assert response.status_code == 200
    value = response.json()["number"]
    assert lower <= value <= upper


def test_random_handles_invalid_bounds():
    # When min >= max the service adjusts bounds to preserve correctness
    lower, upper = 10, 5
    response = client.get(f"/random?min_value={lower}&max_value={upper}")
    assert response.status_code == 200
    assert response.json()["number"] >= lower
