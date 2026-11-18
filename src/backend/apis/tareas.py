from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.tareas import Tarea, TareaCreate, TareaUpdate
from backend.services.tareas import TareaService, tarea_service

router = APIRouter(prefix="/tareas", tags=["tareas"])
ServiceDep = Annotated[TareaService, Depends(lambda: tarea_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("", response_model=list[Tarea])
def listar(service: ServiceDep, user: UserDep) -> list[Tarea]:
    return service.listar(user.id_usuario)


@router.post("", response_model=Tarea, status_code=status.HTTP_201_CREATED)
def crear(datos: TareaCreate, service: ServiceDep, user: UserDep) -> Tarea:
    return service.crear(user.id_usuario, datos)


@router.put("/{id_tarea}", response_model=Tarea)
def actualizar(
    id_tarea: int, datos: TareaUpdate, service: ServiceDep, user: UserDep
) -> Tarea:
    return service.actualizar(id_tarea, user.id_usuario, datos)


@router.delete("/{id_tarea}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_tarea: int, service: ServiceDep, user: UserDep) -> None:
    service.eliminar(id_tarea, user.id_usuario)
