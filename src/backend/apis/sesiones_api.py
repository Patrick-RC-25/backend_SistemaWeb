from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.schemas.sesiones_schema import Sesion, SesionCreate
from backend.services.sesiones_service import SesionService, sesion_service

router = APIRouter(prefix="/sesiones", tags=["sesiones"])


def get_sesion_service() -> SesionService:
    return sesion_service


ServiceDep = Annotated[SesionService, Depends(get_sesion_service)]


@router.get("", response_model=list[Sesion], summary="Listar sesiones")
def listar_sesiones(service: ServiceDep) -> list[Sesion]:
    return service.listar()


@router.post(
    "",
    response_model=Sesion,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una sesión de estudio",
)
def crear_sesion(datos: SesionCreate, service: ServiceDep) -> Sesion:
    return service.crear(datos)


@router.patch(
    "/{sesion_id}/completar",
    response_model=Sesion,
    summary="Marcar sesión como completada",
)
def completar_sesion(sesion_id: int, service: ServiceDep) -> Sesion:
    return service.completar(sesion_id)


@router.patch(
    "/{sesion_id}/cancelar",
    response_model=Sesion,
    summary="Cancelar una sesión",
)
def cancelar_sesion(sesion_id: int, service: ServiceDep) -> Sesion:
    return service.cancelar(sesion_id)
