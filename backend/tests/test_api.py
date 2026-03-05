from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").status_code == 200


def test_compare_versions() -> None:
    response = client.get("/compare", params={"reference": "John 3:16"})
    assert response.status_code == 200
    assert "CUV" in response.json()["versions"]


def test_prayer_endpoint() -> None:
    response = client.get("/prayer", params={"topic": "焦虑"})
    assert response.status_code == 200
    assert len(response.json()["scripture"]) >= 1


def test_discipleship_bounds() -> None:
    response = client.get("/discipleship", params={"weeks": 99})
    assert response.status_code == 200
    assert response.json()["weeks"] == 24


def test_life_scenario() -> None:
    response = client.get("/life-scenario", params={"scenario": "职场"})
    assert response.status_code == 200
    assert len(response.json()["biblical_principles"]) == 3


def test_group_session() -> None:
    response = client.get("/group-session", params={"theme": "安慰"})
    assert response.status_code == 200
    assert len(response.json()["flow"]) == 4


def test_chat_scope_notice() -> None:
    response = client.post("/chat", json={"question": "今天炒股怎么操作"})
    assert response.status_code == 200
    assert response.json()["scope_notice"] is not None
