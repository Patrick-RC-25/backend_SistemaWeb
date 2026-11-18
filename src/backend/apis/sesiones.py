from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.sesiones import Sesion, SesionCreate, SesionUpdate
from backend.services.sesiones import SesionService, sesion_service

router = APIRouter(prefix="/sesiones", tags=["sesiones"])
ServiceDep = Annotated[SesionService, Depends(lambda: sesion_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("", response_model=list[Sesion])
def listar(service: ServiceDep, user: UserDep) -> list[Sesion]:
    return service.listar(user.id_usuario)


@router.get("/hoy", response_model=list[Sesion])
def listar_hoy(service: ServiceDep, user: UserDep) -> list[Sesion]:
    return service.listar_hoy(user.id_usuario)


@router.post("", response_model=Sesion, status_code=status.HTTP_201_CREATED)
def crear(datos: SesionCreate, service: ServiceDep, user: UserDep) -> Sesion:
    return service.crear(user.id_usuario, datos)


@router.put("/{id_sesion}", response_model=Sesion)
def actualizar(
    id_sesion: int, datos: SesionUpdate, service: ServiceDep, user: UserDep
) -> Sesion:
    return service.actualizar(id_sesion, user.id_usuario, datos)


@router.patch("/{id_sesion}/iniciar", response_model=Sesion)
def iniciar(id_sesion: int, service: ServiceDep, user: UserDep) -> Sesion:
    return service.iniciar(id_sesion, user.id_usuario)


@router.patch("/{id_sesion}/finalizar", response_model=Sesion)
def finalizar(id_sesion: int, service: ServiceDep, user: UserDep) -> Sesion:
    return service.finalizar(id_sesion, user.id_usuario)


@router.patch("/{id_sesion}/cancelar", response_model=Sesion)
def cancelar(id_sesion: int, service: ServiceDep, user: UserDep) -> Sesion:
    return service.cancelar(id_sesion, user.id_usuario)


@router.delete("/{id_sesion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_sesion: int, service: ServiceDep, user: UserDep) -> None:
    service.eliminar(id_sesion, user.id_usuario)
