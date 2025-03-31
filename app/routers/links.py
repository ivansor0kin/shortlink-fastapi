from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.database import SessionLocal, get_db
from app.models import Link, User
from app.schemas import LinkCreate, Link as LinkSchema
from app.services import create_link, get_link, delete_link, update_link, get_stats, search_by_url
from app.cache import cache_get, cache_set, cache_delete
from datetime import datetime

router = APIRouter()

@router.get("/search")
def search_link(original_url: str, db: SessionLocal = Depends(get_db)):
    link = search_by_url(db, original_url)
    if link:
        return [{"short_code": link.short_code}]
    raise HTTPException(status_code=404, detail="Link not found")

@router.get("/{short_code}")
def read_link(short_code: str, db: SessionLocal = Depends(get_db)):
    cached_url = cache_get(short_code)
    if cached_url:
        link = db.query(Link).filter(Link.short_code == short_code).first()
        if link:
            link.clicks += 1
            link.last_used = datetime.utcnow()
            db.commit()
        return {"original_url": cached_url}
    link = get_link(db, short_code)
    if link:
        cache_set(link.short_code, link.original_url)
        return {"original_url": link.original_url}
    raise HTTPException(status_code=404, detail="Link not found")

@router.post("/shorten", response_model=LinkSchema)
def shorten_link(link: LinkCreate, user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    new_link = create_link(db, link.original_url, link.custom_alias, link.expires_at, user.id)
    cache_set(new_link.short_code, new_link.original_url)
    return new_link

# @router.get("/{short_code}")
# def read_link(short_code: str, db: SessionLocal = Depends(get_db)):
#     cached_url = cache_get(short_code)
#     if cached_url:
#         link = db.query(Link).filter(Link.short_code == short_code).first()
#         if link:
#             link.clicks += 1
#             link.last_used = datetime.utcnow()
#             db.commit()
#         return {"original_url": cached_url}
#     link = get_link(db, short_code)
#     if link:
#         cache_set(link.short_code, link.original_url)
#         return {"original_url": link.original_url}
#     raise HTTPException(status_code=404, detail="Link not found")

@router.delete("/{short_code}")
def remove_link(short_code: str, user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    if link.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this link")
    delete_link(db, short_code)
    cache_delete(short_code)
    return {"message": "Link deleted"}

@router.put("/{short_code}", response_model=LinkSchema)
def modify_link(short_code: str, link: LinkCreate, user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    link_db = db.query(Link).filter(Link.short_code == short_code).first()
    if not link_db:
        raise HTTPException(status_code=404, detail="Link not found")
    if link_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this link")
    updated_link = update_link(db, short_code, link.original_url)
    cache_set(short_code, updated_link.original_url)
    return updated_link

@router.get("/{short_code}/stats")
def link_stats(short_code: str, db: SessionLocal = Depends(get_db)):
    stats = get_stats(db, short_code)
    if stats:
        return {
            "original_url": stats["original_url"],
            "created_at": stats["created_at"].isoformat(),
            "clicks": stats["clicks"],
            "last_used": stats["last_used"].isoformat() if stats["last_used"] else None
        }
    raise HTTPException(status_code=404, detail="Link not found")

# @router.get("/search")
# def search_link(original_url: str, db: SessionLocal = Depends(get_db)):
#     link = search_by_url(db, original_url)
#     if link:
#         return {"short_code": link.short_code}
#     raise HTTPException(status_code=404, detail="Link not found")