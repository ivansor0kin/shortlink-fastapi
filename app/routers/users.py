from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, get_password_hash, verify_password #убрать из импорта app
from app.database import SessionLocal #убрать из импорта app
from app.models import User #убрать из импорта app
from app.schemas import UserCreate, Token #убрать из импорта app

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        db.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    db.close()
    return {"access_token": access_token, "token_type": "bearer"}