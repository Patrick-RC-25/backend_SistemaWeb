from typing import Annotated
from fastapi import APIRouter, Depends, status
from backend.schemas.cursos_schema import Curso, CursoCreate, CursoUpdate
from backend.services.cursos_service import CursoService, curso_service

router = APIRouter(prefix="/cursos", tags=["cursos"])


def get_curso_service() -> CursoService:
    return curso_service


ServiceDep = Annotated[CursoService, Depends(get_curso_service)]


@router.get("", response_model=list[Curso], summary="Listar cursos")
def listar_cursos(service: ServiceDep) -> list[Curso]:
    return service.listar()


@router.get("/{curso_id}", response_model=Curso, summary="Obtener un curso")
def obtener_curso(curso_id: int, service: ServiceDep) -> Curso:
    return service.obtener(curso_id)


@router.post(
    "",
    response_model=Curso,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un curso",
)
def crear_curso(datos: CursoCreate, service: ServiceDep) -> Curso:
    return service.crear(datos)


@router.put("/{curso_id}", response_model=Curso, summary="Actualizar un curso")
def actualizar_curso(
    curso_id: int, datos: CursoUpdate, service: ServiceDep
) -> Curso:
    return service.actualizar(curso_id, datos)


@router.delete(
    "/{curso_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un curso",
)
def eliminar_curso(curso_id: int, service: ServiceDep) -> None:
    service.eliminar(curso_id)