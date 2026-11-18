from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.alertas import Alerta, AlertaCreate
from backend.services.alertas import AlertaService, alerta_service

router = APIRouter(prefix="/alertas", tags=["alertas"])
ServiceDep = Annotated[AlertaService, Depends(lambda: alerta_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("", response_model=list[Alerta])
def listar(service: ServiceDep, user: UserDep) -> list[Alerta]:
    return service.listar(user.id_usuario)


@router.post("", response_model=Alerta, status_code=status.HTTP_201_CREATED)
def crear(datos: AlertaCreate, service: ServiceDep, user: UserDep) -> Alerta:
    return service.crear(user.id_usuario, datos)


@router.patch("/{id_alerta}/leida", response_model=Alerta)
def marcar_leida(id_alerta: int, service: ServiceDep, user: UserDep) -> Alerta:
    return service.marcar_leida(id_alerta, user.id_usuario)


@router.delete("/{id_alerta}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_alerta: int, service: ServiceDep, user: UserDep) -> None:
    service.eliminar(id_alerta, user.id_usuario)
