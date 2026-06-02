from fastapi import APIRouter, Depends, status
from typing import Optional

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch
)

from app.services.user_service import (
    get_all_users,
    create_user,
    update_user,
    patch_user,
    delete_user
)

from app.dependencies.user_dependencies import get_user_or_404

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    summary="Listar usuarios",
    description="Obtiene todos los usuarios registrados"
)
def get_users(
    role: Optional[str] = None,
    is_active: Optional[bool] = None
):
    return get_all_users(role, is_active)


@router.get(
    "/{user_id}",
    summary="Consultar usuario por ID"
)
def get_user(user: dict = Depends(get_user_or_404)):
    return user


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario"
)
def add_user(user: UserCreate):
    return create_user(user)


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo"
)
def edit_user(
    user_id: int,
    user_data: UserUpdate
):
    return update_user(user_id, user_data)


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente"
)
def update_partial_user(
    user_id: int,
    user_data: UserPatch
):
    return patch_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario"
)
def remove_user(user_id: int):
    return delete_user(user_id)