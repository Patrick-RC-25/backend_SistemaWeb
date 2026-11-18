from typing import Annotated

from fastapi import APIRouter, Depends

from backend.schemas.auth_schema import LoginRequest, LoginResponse
from backend.services.auth_service import AuthService, auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service() -> AuthService:
    return auth_service


ServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/login", response_model=LoginResponse, summary="Iniciar sesión")
def login(datos: LoginRequest, service: ServiceDep) -> LoginResponse:
    return service.login(datos)
