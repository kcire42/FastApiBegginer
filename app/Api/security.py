from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

api_key = "123456789abcdef"

def verify_api_token(token: str = Depends(api_key_header)):
    """Verifica el token de autenticación proporcionado en la solicitud."""
    if token != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return True