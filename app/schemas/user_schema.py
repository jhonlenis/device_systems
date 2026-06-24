<<<<<<< HEAD
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
=======
import re
from datetime import datetime
from typing import Literal, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator
)


class UserBase(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre completo del usuario"
    )

    email: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario"
    )

    role: Literal[
        "admin",
        "support",
        "user"
    ] = Field(
        default="user",
        description="Rol del usuario"
    )

    is_active: bool = Field(
        default=True,
        description="Estado del usuario"
    )


class UserCreate(UserBase):

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Contraseña segura del usuario"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if " " in value:
            raise ValueError(
                "La contraseña no puede contener espacios."
            )

        if len(value) < 8:
            raise ValueError(
                "La contraseña debe tener mínimo 8 caracteres."
            )

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "La contraseña debe contener al menos una mayúscula."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "La contraseña debe contener al menos una minúscula."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "La contraseña debe contener al menos un número."
            )

        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez",
                "email": "juan@sena.edu.co",
                "password": "Password123",
                "role": "admin",
                "is_active": True
            }
        }
    )


class UserUpdate(UserBase):

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Nueva contraseña del usuario"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if " " in value:
            raise ValueError(
                "La contraseña no puede contener espacios."
            )

        if len(value) < 8:
            raise ValueError(
                "La contraseña debe tener mínimo 8 caracteres."
            )

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "La contraseña debe contener al menos una mayúscula."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "La contraseña debe contener al menos una minúscula."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "La contraseña debe contener al menos un número."
            )

        return value


class UserPatch(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
        description="Nombre del usuario"
    )

    email: Optional[EmailStr] = Field(
        default=None,
        description="Correo electrónico"
    )

    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=100,
        description="Nueva contraseña del usuario"
    )

    role: Optional[
        Literal[
            "admin",
            "support",
            "user"
        ]
    ] = Field(
        default=None,
        description="Rol del usuario"
    )

    is_active: Optional[bool] = Field(
        default=None,
        description="Estado del usuario"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: Optional[str]):

        if value is None:
            return value

        if " " in value:
            raise ValueError(
                "La contraseña no puede contener espacios."
            )

        if len(value) < 8:
            raise ValueError(
                "La contraseña debe tener mínimo 8 caracteres."
            )

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "La contraseña debe contener al menos una mayúscula."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "La contraseña debe contener al menos una minúscula."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "La contraseña debe contener al menos un número."
            )

        return value


class UserResponse(BaseModel):

    id: int
>>>>>>> device_systems_security
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

<<<<<<< HEAD

class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
=======
    model_config = ConfigDict(
        from_attributes=True
    )
>>>>>>> device_systems_security
