from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse
)

from app.services.user_service import *


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201
)
def create(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    return create_user(db, user)


@router.get(
    "/",
    response_model=list[UserResponse]
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
    response_model=UserResponse
)
def get_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    return get_user_by_id(
        db,
        user_id
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse
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
    response_model=UserResponse
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


@router.delete("/{user_id}")
def delete(
        user_id: int,
        db: Session = Depends(get_db)
):
    return delete_user(
        db,
        user_id
    )