from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.horarios import Horario, HorarioCreate, HorarioUpdate
from backend.services.horarios import HorarioService, horario_service

router = APIRouter(prefix="/horarios", tags=["horarios"])
ServiceDep = Annotated[HorarioService, Depends(lambda: horario_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("", response_model=list[Horario])
def listar(service: ServiceDep, user: UserDep) -> list[Horario]:
    return service.listar_usuario(user.id_usuario)


@router.get("/curso/{id_curso}", response_model=list[Horario])
def listar_curso(id_curso: int, service: ServiceDep, user: UserDep) -> list[Horario]:
    return service.listar_curso(id_curso, user.id_usuario)


@router.post("", response_model=Horario, status_code=status.HTTP_201_CREATED)
def crear(datos: HorarioCreate, service: ServiceDep, user: UserDep) -> Horario:
    return service.crear(user.id_usuario, datos)


@router.put("/{id_horario}", response_model=Horario)
def actualizar(
    id_horario: int, datos: HorarioUpdate, service: ServiceDep, user: UserDep
) -> Horario:
    return service.actualizar(id_horario, user.id_usuario, datos)


@router.delete("/{id_horario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_horario: int, service: ServiceDep, user: UserDep) -> None:
    service.eliminar(id_horario, user.id_usuario)
