from app.auth import verify_password, get_password_hash, create_access_token, get_current_user
from datetime import timedelta

def test_verify_password():
    password = "test123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False

def test_get_password_hash():
    password = "test123"
    hashed = get_password_hash(password)
    assert isinstance(hashed, str)
    assert len(hashed) > 0

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=1))
    assert isinstance(token, str)
    assert len(token) > 0

def test_get_current_user(db_session, test_user):
    token = create_access_token({"sub": test_user.username})
    user = get_current_user(token=token)
    assert user.username == "testuser"