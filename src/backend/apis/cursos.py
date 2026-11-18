from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.cursos import Curso, CursoCreate, CursoUpdate
from backend.services.cursos import CursoService, curso_service

router = APIRouter(prefix="/cursos", tags=["cursos"])
ServiceDep = Annotated[CursoService, Depends(lambda: curso_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("", response_model=list[Curso])
def listar(service: ServiceDep, user: UserDep) -> list[Curso]:
    return service.listar(user.id_usuario)


@router.get("/{id_curso}", response_model=Curso)
def obtener(id_curso: int, service: ServiceDep, user: UserDep) -> Curso:
    return service.obtener(id_curso, user.id_usuario)


@router.post("", response_model=Curso, status_code=status.HTTP_201_CREATED)
def crear(datos: CursoCreate, service: ServiceDep, user: UserDep) -> Curso:
    return service.crear(user.id_usuario, datos)


@router.put("/{id_curso}", response_model=Curso)
def actualizar(
    id_curso: int, datos: CursoUpdate, service: ServiceDep, user: UserDep
) -> Curso:
    return service.actualizar(id_curso, user.id_usuario, datos)


@router.delete("/{id_curso}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_curso: int, service: ServiceDep, user: UserDep) -> None:
    service.eliminar(id_curso, user.id_usuario)
