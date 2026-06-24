import logging
import time
import uuid

from fastapi import Request

# =====================================================
# Configuración del logger
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("device_systems")


async def request_middleware(
    request: Request,
    call_next
):
    """
    Middleware global.

    Funciones:
    - Medir tiempo de respuesta.
    - Registrar peticiones.
    - Agregar cabeceras personalizadas.
    - Generar o propagar X-Request-ID.
    """

    start_time = time.perf_counter()

    # Obtener Request ID o generar uno nuevo
    request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4())
    )

    # Procesar la petición
    response = await call_next(request)

    process_time = round(
        time.perf_counter() - start_time,
        4
    )

    # Cabeceras personalizadas
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id

    # Registrar información de la petición
    logger.info(
        (
            f"{request.method} | "
            f"{request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time}s | "
            f"Request-ID: {request_id}"
        )
    )

    return response