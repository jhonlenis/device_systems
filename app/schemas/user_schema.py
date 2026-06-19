from datetime import datetime
from typing import Literal, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


class UserCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
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
        ...,
        description="Rol del usuario"
    )

    is_active: bool = Field(
        default=True,
        description="Estado del usuario"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez",
                "email": "juan@sena.edu.co",
                "role": "user",
                "is_active": True
            }
        }
    )


class UserUpdate(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        description="Nombre completo del usuario"
    )

    email: EmailStr

    role: Literal[
        "admin",
        "support",
        "user"
    ]

    is_active: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez",
                "email": "juan@sena.edu.co",
                "role": "support",
                "is_active": True
            }
        }
    )


class UserPatch(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        description="Nombre del usuario"
    )

    email: Optional[EmailStr] = None

    role: Optional[
        Literal[
            "admin",
            "support",
            "user"
        ]
    ] = None

    is_active: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "admin"
            }
        }
    )


class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )