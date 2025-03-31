# tests/test_extra.py
import pytest
from datetime import datetime, timedelta
from app.services import (
    create_link,
    update_link,
    get_stats,
    delete_link,
    normalize_url,
)
from app.database import get_db
from app.models import Link

def test_update_link_success(db_session):
    # Создаем ссылку
    link = create_link(db_session, "https://example.com", short_code="testup", user_id=1)
    new_url = "https://newexample.com"
    updated = update_link(db_session, "testup", original_url=new_url)
    assert updated is not None
    # Проверяем, что ссылка нормализована (без завершающего слэша)
    assert updated.original_url == normalize_url(new_url)

def test_update_link_not_found(db_session):
    updated = update_link(db_session, "nonexistent", original_url="https://newexample.com")
    assert updated is None

def test_update_link_with_expires(db_session):
    # Создаем ссылку без указанного expires_at
    link = create_link(db_session, "https://example.com", short_code="expiretest", user_id=1)
    new_expiry = datetime.utcnow() + timedelta(days=10)
    updated = update_link(db_session, "expiretest", expires_at=new_expiry)
    assert updated is not None
    # Проверяем, что expires_at обновился (с допуском в 1 секунду)
    assert abs((updated.expires_at - new_expiry).total_seconds()) < 1

def test_get_stats_success(db_session):
    link = create_link(db_session, "https://example.com", short_code="teststat", user_id=1)
    stats = get_stats(db_session, "teststat")
    assert stats is not None
    assert stats["short_code"] == "teststat"
    assert "original_url" in stats
    assert isinstance(stats["clicks"], int)
    # created_at, expires_at, last_used могут быть None или datetime

def test_get_stats_not_found(db_session):
    stats = get_stats(db_session, "nonexistent")
    assert stats is None

def test_delete_link_not_found(db_session):
    result = delete_link(db_session, "nonexistent")
    assert result is False

def test_get_db_functionality(db_session):
    # Проверяем работу функции get_db
    db_gen = get_db()
    db_instance = next(db_gen)
    # Выполняем простой запрос: так как таблица Link может быть пустой, ожидаем пустой список
    result = db_instance.query(Link).all()
    # Завершаем генератор; ожидаем StopIteration, если генератор завершен корректно
    with pytest.raises(StopIteration):
        next(db_gen)