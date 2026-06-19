from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.models.loan_model import Loan


def create_user(
    db: Session,
    user
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    new_user = User(
        name=user.name,
        email=user.email,
        role=user.role,
        is_active=user.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_users(
    db: Session,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    order_by: Optional[str] = None
):

    query = db.query(User)

    if role:
        query = query.filter(
            User.role == role
        )

    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    # Validar campo de ordenamiento
    valid_orders = [
        "name",
        "created_at"
    ]

    if order_by:

        if order_by not in valid_orders:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campo de ordenamiento inválido."
            )

        if order_by == "name":
            query = query.order_by(
                User.name
            )

        elif order_by == "created_at":
            query = query.order_by(
                User.created_at
            )

    return query.all()


def get_user_by_id(
    db: Session,
    user_id: int
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

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

    user = get_user_by_id(
        db,
        user_id
    )

    duplicate = db.query(User).filter(
        User.email == user_data.email,
        User.id != user_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    user.name = user_data.name
    user.email = user_data.email
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

    user = get_user_by_id(
        db,
        user_id
    )

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    if "email" in update_data:

        duplicate = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )

    for key, value in update_data.items():
        setattr(
            user,
            key,
            value
        )

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user_id: int
):

    user = get_user_by_id(
        db,
        user_id
    )

    db.delete(user)
    db.commit()

    return {
        "message": "Usuario eliminado correctamente."
    }


def get_user_loans(
    db: Session,
    user_id: int
):

    user = get_user_by_id(
        db,
        user_id
    )

    loans = (
        db.query(Loan)
        .filter(
            Loan.user_id == user.id
        )
        .all()
    )

    return loans