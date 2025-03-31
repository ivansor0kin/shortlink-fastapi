from app.services import create_link
from app.auth import create_access_token

def test_create_link(client, db_session, test_user, mocker):
    token = create_access_token({"sub": test_user.username})
    client.headers["Authorization"] = f"Bearer {token}"
    mocker.patch("app.routers.links.get_current_user", return_value=test_user)  # Мокаем авторизацию
    mocker.patch("app.cache.cache_set", return_value=None)  # Мокаем cache_set
    response = client.post("/links/shorten", json={"original_url": "https://example.com"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert "short_code" in data
    assert data["original_url"] == "https://example.com"

def test_create_link_invalid_url(client, db_session, test_user):
    token = create_access_token({"sub": test_user.username})
    client.headers["Authorization"] = f"Bearer {token}"
    response = client.post("/links/shorten", json={"original_url": "not-a-url"})
    assert response.status_code == 422, f"Expected 422, got {response.status_code}: {response.text}"

def test_get_link(client, db_session):
    create_link(db_session, "https://example.com", short_code="exmpl")
    response = client.get("/links/exmpl")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json()["original_url"] == "https://example.com"

def test_get_link_not_found(client):
    response = client.get("/links/nonexistent")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.text}"
    assert response.json()["detail"] == "Link not found"

def test_delete_link(client, db_session, test_user):
    token = create_access_token({"sub": test_user.username})
    client.headers["Authorization"] = f"Bearer {token}"
    link = create_link(db_session, "https://example.com", short_code="exmpl", user_id=test_user.id)
    response = client.delete(f"/links/{link.short_code}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json()["message"] == "Link deleted"

def test_search_link(client, db_session):
    create_link(db_session, "https://stepik.org/learn", short_code="stepik")
    response = client.get("/links/search?original_url=https://stepik.org/learn")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert len(data) == 1
    assert data[0]["short_code"] == "stepik"