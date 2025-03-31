from app.services import normalize_url, create_link, get_link, search_by_url
from app.models import Link
from datetime import datetime
from urllib.parse import urlparse, urlunparse
import pytest

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    scheme = "https"
    path = parsed.path.rstrip('/')
    return urlunparse((scheme, parsed.netloc, path, '', '', ''))

def test_create_link(db_session):
    link = create_link(db_session, "https://example.com", short_code="exmpl", user_id=1)
    assert link.original_url == "https://example.com"
    assert link.short_code == "exmpl"
    assert link.user_id == 1

def test_create_link_duplicate_short_code(db_session):
    create_link(db_session, "https://example.com", short_code="exmpl")
    with pytest.raises(ValueError, match="Short code already exists"):
        create_link(db_session, "https://test.com", short_code="exmpl")

def test_get_link_expired(db_session):
    link = create_link(db_session, "https://example.com", short_code="exmpl", expires_at=datetime(2020, 1, 1))
    result = get_link(db_session, "exmpl")
    assert result is None
    assert db_session.query(Link).filter(Link.short_code == "exmpl").first() is None

def test_search_by_url(db_session):
    create_link(db_session, "https://stepik.org/learn", short_code="stepik")
    link = search_by_url(db_session, "https://stepik.org/learn/")
    assert link is not None
    assert link.short_code == "stepik"