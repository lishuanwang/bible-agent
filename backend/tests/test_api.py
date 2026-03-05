from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_verse_found() -> None:
    response = client.get("/verse", params={"reference": "John 3:16"})
    assert response.status_code == 200
    assert response.json()["reference"] == "John 3:16"


def test_chat_risk_notice() -> None:
    response = client.post("/chat", json={"question": "我有自杀念头"})
    assert response.status_code == 200
    assert response.json()["safety_notice"] is not None
