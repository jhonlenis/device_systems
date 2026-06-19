from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class DeviceBase(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        description="Nombre del dispositivo"
    )

    serial_number: str = Field(
        ...,
        description="Número de serie único del dispositivo"
    )

    device_type: str = Field(
        ...,
        description="Tipo de dispositivo (laptop, tablet, monitor, router, cámara, etc.)"
    )

    brand: Optional[str] = Field(
        default=None,
        description="Marca del dispositivo"
    )


class DeviceCreate(DeviceBase):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Lenovo ThinkPad",
                "serial_number": "LEN-2026-001",
                "device_type": "laptop",
                "brand": "Lenovo"
            }
        }
    )


class DeviceUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        description="Nombre del dispositivo"
    )

    serial_number: Optional[str] = Field(
        default=None,
        description="Número de serie"
    )

    device_type: Optional[str] = Field(
        default=None,
        description="Tipo del dispositivo"
    )

    brand: Optional[str] = Field(
        default=None,
        description="Marca del dispositivo"
    )

    is_available: Optional[bool] = Field(
        default=None,
        description="Disponibilidad del dispositivo"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "brand": "Dell",
                "is_available": True
            }
        }
    )


class DeviceResponse(DeviceBase):

    id: int
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )