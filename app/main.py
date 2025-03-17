from fastapi import FastAPI
from .routers import links, users
from .database import Base, engine

app = FastAPI()

# Создание таблиц в базе данных при запуске
Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="")
app.include_router(links.router, prefix="/links")