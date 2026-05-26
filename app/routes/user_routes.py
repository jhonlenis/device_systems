from fastapi import APIRouter, HTTPException, Query, Response
from typing import Optional
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# In-memory "database"
users_db: list[dict] = [
    {"id": 1, "name": "Ana García",    "email": "ana@devicesystems.com",   "role": "admin",   "is_active": True},
    {"id": 2, "name": "Carlos López",  "email": "carlos@devicesystems.com","role": "support", "is_active": True},
    {"id": 3, "name": "María Ruiz",    "email": "maria@devicesystems.com", "role": "user",    "is_active": False},
    {"id": 4, "name": "Pedro Torres",  "email": "pedro@devicesystems.com", "role": "user",    "is_active": True},
]

_counter = {"id": len(users_db)}


def _custom_headers(response: Response) -> None:
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "1.0"


# ── GET /users ────────────────────────────────────────────────────────────────
@router.get("/", response_model=list[UserResponse], summary="Listar usuarios")
def list_users(
    response: Response,
    role:      Optional[str]  = Query(None, description="Filtrar por rol: admin | support | user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
):
    """
    Retorna todos los usuarios.  
    Acepta query params opcionales:
    - **role** → filtra por rol  
    - **is_active** → filtra por estado
    """
    _custom_headers(response)
    result = users_db

    if role is not None:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]

    return result


# ── GET /users/{user_id} ──────────────────────────────────────────────────────
@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID")
def get_user(user_id: int, response: Response):
    """Retorna un usuario específico usando su **ID** como path parameter."""
    _custom_headers(response)
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail=f"Usuario con id={user_id} no encontrado.")


# ── POST /users ───────────────────────────────────────────────────────────────
@router.post("/", response_model=UserResponse, status_code=201, summary="Crear usuario")
def create_user(user: UserCreate, response: Response):
    """
    Registra un nuevo usuario.  
    - Valida los datos con **Pydantic v2**  
    - Rechaza correos duplicados
    """
    _custom_headers(response)

    # Duplicate email check
    for existing in users_db:
        if existing["email"] == user.email:
            raise HTTPException(
                status_code=409,
                detail=f"Ya existe un usuario con el correo '{user.email}'.",
            )

    _counter["id"] += 1
    new_user = {
        "id":        _counter["id"],
        "name":      user.name,
        "email":     user.email,
        "role":      user.role,
        "is_active": user.is_active,
    }
    users_db.append(new_user)
    return new_user
