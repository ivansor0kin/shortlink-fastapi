from .models import Link
from .utils import generate_short_code
from .config import DEFAULT_LINK_EXPIRY_DAYS
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

def create_link(db: Session, original_url: str, custom_alias: str = None, expires_at: datetime = None,
                user_id: int = None):
    if custom_alias:
        if db.query(Link).filter(Link.short_code == custom_alias).first():
            raise ValueError("Custom alias already exists")
        short_code = custom_alias
    else:
        short_code = generate_short_code()
        while db.query(Link).filter(Link.short_code == short_code).first():
            short_code = generate_short_code()

    if not expires_at:
        expires_at = datetime.utcnow() + timedelta(days=DEFAULT_LINK_EXPIRY_DAYS)

    link = Link(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at,
        user_id=user_id
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

def get_link(db: Session, short_code: str):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if link and (not link.expires_at or link.expires_at > datetime.utcnow()):
        link.clicks += 1
        link.last_used = datetime.utcnow()
        db.commit()
        return link
    return None

def delete_link(db: Session, short_code: str):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if link:
        db.delete(link)
        db.commit()

def update_link(db: Session, short_code: str, new_url: str):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if link:
        link.original_url = new_url
        db.commit()
        db.refresh(link)
        return link
    return None

def get_stats(db: Session, short_code: str):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if link:
        return {
            "original_url": link.original_url,
            "created_at": link.created_at,
            "clicks": link.clicks,
            "last_used": link.last_used
        }
    return None

def search_by_url(db: Session, original_url: str):
    return db.query(Link).filter(Link.original_url == original_url).first()