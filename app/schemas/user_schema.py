from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v: str) -> str:
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres.")
        return v.strip()


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

    model_config = {"from_attributes": True}
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict
)

from typing import Optional
from typing import Literal

from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3
    )

    email: EmailStr

    role: Literal[
        "admin",
        "support",
        "user"
    ]

    is_active: bool = True


class UserUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=3
    )

    email: EmailStr

    role: Literal[
        "admin",
        "support",
        "user"
    ]

    is_active: bool


class UserPatch(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=3
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


class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime