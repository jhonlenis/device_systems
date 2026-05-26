from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**.\n\n"
        "Desarrollada con FastAPI + Pydantic v2."
    ),
    version="1.0.0",
    contact={"name": "device_systems Team"},
)

app.include_router(user_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app":     "device_systems",
        "version": "1.0.0",
        "docs":    "/docs",
    }
