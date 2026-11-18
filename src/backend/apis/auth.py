from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.apis.deps import get_current_user
from backend.schemas.auth import (
    TokenResponse,
    UsuarioLogin,
    UsuarioRegistro,
    UsuarioResponse,
)
from backend.services.auth import AuthService, auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

AuthDep = Annotated[AuthService, Depends(lambda: auth_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(datos: UsuarioRegistro, service: AuthDep) -> TokenResponse:
    return service.registrar(datos)


@router.post("/login", response_model=TokenResponse)
def login(datos: UsuarioLogin, service: AuthDep) -> TokenResponse:
    return service.login(datos)


@router.get("/me", response_model=UsuarioResponse)
def me(user: UserDep) -> UsuarioResponse:
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(_user: UserDep) -> None:
    # JWT stateless: el cliente elimina el token
    return None
