from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.objetivos import Objetivo, ObjetivoCreate, ObjetivoUpdate
from backend.services.objetivos import ObjetivoService, objetivo_service

router = APIRouter(prefix="/objetivos", tags=["objetivos"])
ServiceDep = Annotated[ObjetivoService, Depends(lambda: objetivo_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("", response_model=list[Objetivo])
def listar(service: ServiceDep, user: UserDep) -> list[Objetivo]:
    return service.listar(user.id_usuario)


@router.post("", response_model=Objetivo, status_code=status.HTTP_201_CREATED)
def crear(datos: ObjetivoCreate, service: ServiceDep, user: UserDep) -> Objetivo:
    return service.crear(user.id_usuario, datos)


@router.put("/{id_objetivo}", response_model=Objetivo)
def actualizar(
    id_objetivo: int, datos: ObjetivoUpdate, service: ServiceDep, user: UserDep
) -> Objetivo:
    return service.actualizar(id_objetivo, user.id_usuario, datos)


@router.delete("/{id_objetivo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_objetivo: int, service: ServiceDep, user: UserDep) -> None:
    service.eliminar(id_objetivo, user.id_usuario)
