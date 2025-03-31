def test_register_user(client):
    response = client.post("/register", json={"username": "newuser", "password": "newpass123"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert "access_token" in data

def test_register_user_duplicate(client, test_user):
    response = client.post("/register", json={"username": "testuser", "password": "test123"})
    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
    assert response.json()["detail"] == "Username already registered"

def test_login(client, test_user):
    response = client.post("/token", data={"username": "testuser", "password": "test123"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert "access_token" in data

def test_login_invalid_credentials(client):
    response = client.post("/token", data={"username": "wronguser", "password": "wrongpass"})
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
    assert response.json()["detail"] == "Incorrect username or password"