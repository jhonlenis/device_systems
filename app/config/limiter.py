from slowapi import Limiter
from slowapi.util import get_remote_address

# =====================================================
# Configuración global de Rate Limiting
# =====================================================

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"]
)