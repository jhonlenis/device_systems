from fastapi import FastAPI

from app.database.connection import (
    engine,
    Base
)

from app.models.user_model import User

from app.routes.user_routes import (
    router
)

Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Device Systems API",
    description="CRUD de usuarios usando FastAPI + SQLAlchemy + PostgreSQL Neon",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message":
        "Device Systems API funcionando correctamente"
    }