from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import Response
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse
)

from app.schemas.loan_schema import LoanDetailResponse

from app.services.device_service import (
    create_device,
    get_devices,
    get_device_by_id,
    update_device,
    patch_device,
    delete_device,
    get_device_loans
)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo tecnológico en el sistema.",
    response_description="Dispositivo creado correctamente.",
    responses={
        201: {"description": "Dispositivo creado correctamente."},
        400: {"description": "El número de serie ya está registrado."},
        422: {"description": "Error de validación."}
    }
)
def create(
    device: DeviceCreate,
    db: Session = Depends(get_db)
):
    return create_device(
        db,
        device
    )


@router.get(
    "",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Obtiene todos los dispositivos registrados. Permite filtrar por tipo, marca, disponibilidad o realizar búsquedas.",
    response_description="Lista de dispositivos obtenida correctamente."
)
def read_all(
    device_type: Optional[str] = None,
    brand: Optional[str] = None,
    is_available: Optional[bool] = Query(default=None),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_devices(
        db,
        device_type,
        brand,
        is_available,
        search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo por ID",
    description="Obtiene la información de un dispositivo mediante su identificador.",
    response_description="Dispositivo encontrado.",
    responses={
        404: {"description": "Dispositivo no encontrado."}
    }
)
def read_one(
    device_id: int,
    db: Session = Depends(get_db)
):
    return get_device_by_id(
        db,
        device_id
    )


@router.get(
    "/{device_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Consultar historial de préstamos del dispositivo",
    description="Obtiene el historial completo de préstamos asociados a un dispositivo.",
    response_description="Historial de préstamos obtenido correctamente.",
    responses={
        404: {"description": "Dispositivo no encontrado."}
    }
)
def device_loans(
    device_id: int,
    db: Session = Depends(get_db)
):
    return get_device_loans(
        db,
        device_id
    )


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo",
    description="Actualiza completamente la información de un dispositivo.",
    response_description="Dispositivo actualizado correctamente.",
    responses={
        400: {"description": "Número de serie duplicado."},
        404: {"description": "Dispositivo no encontrado."},
        422: {"description": "Error de validación."}
    }
)
def update(
    device_id: int,
    device: DeviceCreate,
    db: Session = Depends(get_db)
):
    return update_device(
        db,
        device_id,
        device
    )


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar parcialmente un dispositivo",
    description="Actualiza uno o varios campos de un dispositivo.",
    response_description="Dispositivo actualizado correctamente.",
    responses={
        400: {"description": "Número de serie duplicado."},
        404: {"description": "Dispositivo no encontrado."},
        422: {"description": "Error de validación."}
    }
)
def patch(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db)
):
    return patch_device(
        db,
        device_id,
        device
    )


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo del sistema.",
    response_description="Dispositivo eliminado correctamente.",
    responses={
        204: {"description": "Dispositivo eliminado correctamente."},
        404: {"description": "Dispositivo no encontrado."}
    }
)
def delete(
    device_id: int,
    db: Session = Depends(get_db)
):
    delete_device(
        db,
        device_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )