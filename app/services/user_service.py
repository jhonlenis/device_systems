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

    return new_user


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