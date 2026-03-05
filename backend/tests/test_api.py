from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_verse_found() -> None:
    response = client.get("/verse", params={"reference": "John 3:16", "translation": "CUV"})
    assert response.status_code == 200
    assert response.json()["reference"] == "John 3:16"


def test_compare_versions() -> None:
    response = client.get("/compare", params={"reference": "John 3:16"})
    assert response.status_code == 200
    assert "CUV" in response.json()["versions"]
    assert "NIV" in response.json()["versions"]


def test_context_found() -> None:
    response = client.get("/context", params={"reference": "John 3:16"})
    assert response.status_code == 200
    assert response.json()["book"] == "John"


def test_topic_study() -> None:
    response = client.get("/topic", params={"topic": "安慰"})
    assert response.status_code == 200
    assert len(response.json()["key_verses"]) >= 1


def test_devotional_plan_days_limit() -> None:
    response = client.get("/devotional", params={"theme": "安慰", "days": 40})
    assert response.status_code == 200
    assert response.json()["days"] == 30


def test_sermon_outline() -> None:
    response = client.get("/sermon", params={"reference": "John 3:16"})
    assert response.status_code == 200
    assert len(response.json()["outline"]) == 3


def test_chat_risk_notice() -> None:
    response = client.post("/chat", json={"question": "我有自杀念头"})
    assert response.status_code == 200
    assert response.json()["safety_notice"] is not None
