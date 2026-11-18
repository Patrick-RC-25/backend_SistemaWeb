from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from backend.core.security import decode_access_token
from backend.repositories.usuarios import UsuarioRepository, usuario_repository
from backend.schemas.auth import UsuarioResponse

security_bearer = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_bearer)],
    repo: Annotated[UsuarioRepository, Depends(lambda: usuario_repository)],
) -> UsuarioResponse:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email or not isinstance(email, str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token de autenticación ha expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = repo.get_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    id_usuario, user_email, _ = user
    return UsuarioResponse(id_usuario=id_usuario, email=user_email)
