<<<<<<< HEAD
from fastapi import HTTPException

from app.data.users_db import users_db

from app.dependencies.user_dependencies import (
    validate_email_exists,
    validate_role
)


def get_all_users(role: str = None, is_active: bool = None):
    users = users_db

    if role:
        users = [user for user in users if user["role"] == role]

    if is_active is not None:
        users = [user for user in users if user["is_active"] == is_active]

    return users


def create_user(user_data):
    validate_role(user_data.role)
    validate_email_exists(user_data.email)

    new_user = {
        "id": len(users_db) + 1,
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "is_active": user_data.is_active
    }

    users_db.append(new_user)
=======
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import get_password_hash
from app.models.user_model import User


def create_user(
    db: Session,
    user
):
    existing = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role,
        is_active=user.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
>>>>>>> device_systems_security

    return new_user


<<<<<<< HEAD
def update_user(user_id: int, user_data):
    validate_role(user_data.role)
    validate_email_exists(user_data.email, user_id)

    for user in users_db:
        if user["id"] == user_id:
            user["name"] = user_data.name
            user["email"] = user_data.email
            user["role"] = user_data.role
            user["is_active"] = user_data.is_active

            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


def patch_user(user_id: int, user_data):
    data = user_data.dict(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar"
        )

    for user in users_db:
        if user["id"] == user_id:

            if "role" in data:
                validate_role(data["role"])

            if "email" in data:
                validate_email_exists(data["email"], user_id)

            user.update(data)
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


def delete_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            users_db.remove(user)
            return {
                "message": "Usuario eliminado correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
=======
def get_users(
    db: Session,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    order_by: Optional[str] = None
):
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    valid_orders = ["name", "created_at"]

    if order_by:
        if order_by not in valid_orders:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campo de ordenamiento inválido."
            )

        if order_by == "name":
            query = query.order_by(User.name)

        elif order_by == "created_at":
            query = query.order_by(User.created_at)

    return query.all()


def get_user_by_id(
    db: Session,
    user_id: int
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    return user


def update_user(
    db: Session,
    user_id: int,
    user_data
):
    user = get_user_by_id(db, user_id)

    duplicate = (
        db.query(User)
        .filter(
            User.email == user_data.email,
            User.id != user_id
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    user.name = user_data.name
    user.email = user_data.email
    user.hashed_password = get_password_hash(user_data.password)
    user.role = user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user


def patch_user(
    db: Session,
    user_id: int,
    user_data
):
    user = get_user_by_id(db, user_id)

    update_data = user_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        duplicate = (
            db.query(User)
            .filter(
                User.email == update_data["email"],
                User.id != user_id
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user_id: int
):
    user = get_user_by_id(db, user_id)

    db.delete(user)
    db.commit()

    return {
        "message": "Usuario eliminado correctamente."
    }
>>>>>>> device_systems_security
