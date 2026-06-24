import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware

from app.config.limiter import limiter
from app.database.connection import Base, engine

# Modelos
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

# Rutas
from app.auth.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.routes.security_routes import router as security_router

# Middleware personalizado
from app.middlewares.request_middleware import request_middleware


# =====================================================
# Crear tablas solo en desarrollo
# En producción usar exclusivamente Alembic
# =====================================================

if os.getenv("ENV", "development") == "development":
    Base.metadata.create_all(bind=engine)


# =====================================================
# Aplicación FastAPI
# =====================================================

app = FastAPI(
    title="device_systems API",
    description="""
API REST segura para la gestión de usuarios, dispositivos y préstamos.

## Características principales
- Autenticación con OAuth2 + JWT
- Hash de contraseñas con Passlib (bcrypt)
- CRUD de usuarios, dispositivos y préstamos
- Validaciones avanzadas con Pydantic v2
- Protección de rutas por roles
- Configuración CORS
- Middleware personalizado
- Rate limiting con SlowAPI
- Documentación automática con Swagger y ReDoc
""",
    version="3.1.0",
    contact={
        "name": "Jhon Lenis",
        "email": "aprendiz@sena.edu.co"
    },
    license_info={
        "name": "MIT License"
    },
    openapi_tags=[
        {
            "name": "Home",
            "description": "Información general y estado de la API."
        },
        {
            "name": "Auth",
            "description": "Autenticación, registro, login y consulta del usuario autenticado."
        },
        {
            "name": "Users",
            "description": "Gestión de usuarios del sistema."
        },
        {
            "name": "Devices",
            "description": "Gestión de dispositivos tecnológicos."
        },
        {
            "name": "Loans",
            "description": "Gestión de préstamos de dispositivos."
        },
        {
            "name": "Security",
            "description": "Información de seguridad, autenticación y protección de la API."
        }
    ],
    docs_url="/docs",
    redoc_url="/redoc"
)


# =====================================================
# Rate Limiting (SlowAPI)
# =====================================================

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
app.add_middleware(SlowAPIMiddleware)


# =====================================================
# Configuración CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =====================================================
# Middleware personalizado
# =====================================================

app.middleware("http")(request_middleware)


# =====================================================
# Registro de rutas
# =====================================================

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)
app.include_router(security_router)


# =====================================================
# Endpoint principal
# =====================================================

@app.get(
    "/",
    tags=["Home"],
    summary="Inicio de la API",
    description="Muestra información general sobre la API device_systems y sus módulos principales."
)
def root():
    return {
        "application": "device_systems",
        "version": "3.1.0",
        "status": "OK",
        "security": {
            "authentication": "OAuth2 + JWT",
            "password_hash": "Passlib (bcrypt)",
            "cors": True,
            "middleware": True,
            "rate_limiting": True
        },
        "database": {
            "engine": "SQLite",
            "orm": "SQLAlchemy",
            "migrations": "Alembic"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "modules": [
            "Auth",
            "Users",
            "Devices",
            "Loans",
            "Security"
        ]
    }