import os
# Устанавливаем SECRET_KEY до любых импортов
os.environ["SECRET_KEY"] = "0cc91c437e6f60fff6e68f2e9ff9575bb70ed1a524c00c1048643005a37f30d1"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db
from app.models import User, Link
from app.auth import get_password_hash

# Тестовая база данных (in-memory SQLite для скорости)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Переопределяем глобальную сессию в auth.py на тестовую
from app import auth
auth.SessionLocal = TestingSessionLocal

@pytest.fixture(scope="function")
def db_session():
    """Создаёт временную БД для каждого теста."""
    Base.metadata.drop_all(bind=engine)  # Удаляем таблицы перед созданием
    Base.metadata.create_all(bind=engine)  # Создаём таблицы перед тестом
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session, mocker):
    """Фикстура для TestClient с подменой зависимостей."""
    def override_get_db():
        yield db_session  # <-- изменено: больше не закрываем сессию здесь

    app.dependency_overrides[get_db] = override_get_db
    # Мокаем Redis
    mocker.patch('app.cache.redis_client.get', return_value=None)
    mocker.patch('app.cache.redis_client.setex', return_value=None)
    mocker.patch('app.cache.redis_client.delete', return_value=None)

    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """Создаёт тестового пользователя."""
    hashed_password = get_password_hash("test123")
    user = User(username="testuser", hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user