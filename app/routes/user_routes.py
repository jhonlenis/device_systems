from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse
)

from app.schemas.loan_schema import LoanDetailResponse

from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    update_user,
    patch_user,
    delete_user,
    get_user_loans
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un usuario",
    description="Registra un nuevo usuario en el sistema.",
    response_description="Usuario creado correctamente.",
    responses={
        201: {"description": "Usuario creado correctamente."},
        400: {"description": "El correo electrónico ya está registrado."},
        422: {"description": "Error de validación."}
    }
)
def create(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(
        db,
        user
    )


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios registrados. Permite filtrar por rol, estado y ordenar los resultados.",
    response_description="Lista de usuarios obtenida correctamente."
)
def list_users(
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    order_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_users(
        db,
        role,
        is_active,
        order_by
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario por ID",
    description="Obtiene la información de un usuario mediante su identificador.",
    response_description="Usuario encontrado.",
    responses={
        404: {"description": "Usuario no encontrado."}
    }
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_by_id(
        db,
        user_id
    )


@router.get(
    "/{user_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Consultar préstamos de un usuario",
    description="Obtiene el historial de préstamos realizados por un usuario.",
    response_description="Historial de préstamos obtenido correctamente.",
    responses={
        404: {"description": "Usuario no encontrado."}
    }
)
def user_loans(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_loans(
        db,
        user_id
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Actualiza completamente la información de un usuario.",
    response_description="Usuario actualizado correctamente.",
    responses={
        400: {"description": "Correo electrónico duplicado."},
        404: {"description": "Usuario no encontrado."},
        422: {"description": "Error de validación."}
    }
)
def update(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    return update_user(
        db,
        user_id,
        user
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar parcialmente un usuario",
    description="Actualiza uno o varios campos de un usuario.",
    response_description="Usuario actualizado correctamente.",
    responses={
        400: {"description": "Correo electrónico duplicado."},
        404: {"description": "Usuario no encontrado."},
        422: {"description": "Error de validación."}
    }
)
def patch(
    user_id: int,
    user: UserPatch,
    db: Session = Depends(get_db)
):
    return patch_user(
        db,
        user_id,
        user
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema.",
    response_description="Usuario eliminado correctamente.",
    responses={
        204: {"description": "Usuario eliminado correctamente."},
        404: {"description": "Usuario no encontrado."}
    }
)
def delete(
    user_id: int,
    db: Session = Depends(get_db)
):
    delete_user(
        db,
        user_id
    )