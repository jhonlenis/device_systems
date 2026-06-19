from fastapi import FastAPI

from app.database.connection import Base, engine

# Modelos
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

# Rutas
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# Crear tablas (solo para desarrollo.
# En producción las migraciones se realizan con Alembic.)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Systems API",
    version="2.0.0",
    description="""
## API REST para la gestión de dispositivos tecnológicos

Esta API permite administrar:

- 👤 Usuarios
- 💻 Dispositivos
- 📋 Préstamos

### Tecnologías utilizadas

- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic

### Funcionalidades

- CRUD completo de usuarios.
- CRUD completo de dispositivos.
- Gestión de préstamos.
- Relaciones entre tablas.
- Consultas con JOIN.
- Filtros avanzados.
- Validaciones.
- Manejo de errores HTTP.
- Documentación automática con Swagger y ReDoc.
""",
    contact={
        "name": "Jhon Lenis",
        "email": "aprendiz@sena.edu.co"
    },
    license_info={
        "name": "MIT License"
    },
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operaciones relacionadas con la gestión de usuarios."
        },
        {
            "name": "Devices",
            "description": "Operaciones relacionadas con los dispositivos tecnológicos."
        },
        {
            "name": "Loans",
            "description": "Operaciones relacionadas con los préstamos de dispositivos."
        },
        {
            "name": "Home",
            "description": "Información general de la API."
        }
    ],
    docs_url="/docs",
    redoc_url="/redoc"
)

# Registrar rutas
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get(
    "/",
    tags=["Home"],
    summary="Verificar estado de la API",
    description="Permite comprobar que la API se encuentra funcionando correctamente.",
    response_description="Información general de la API."
)
def root():
    return {
        "message": "Device Systems API funcionando correctamente",
        "version": "2.0.0",
        "database": "SQLite",
        "orm": "SQLAlchemy",
        "migrations": "Alembic",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "modules": [
            "Users",
            "Devices",
            "Loans"
        ],
        "status": "OK"
    }