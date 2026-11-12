from typing import Annotated
from fastapi import APIRouter, Depends, status
from backend.schemas.notas_schema import Nota, NotaCreate, NotaUpdate
from backend.services.notas_service import NotaService, nota_service

router = APIRouter(prefix="/notas", tags=["notas"])


def get_nota_service() -> NotaService:
    return nota_service


ServiceDep = Annotated[NotaService, Depends(get_nota_service)]


@router.get("", response_model=list[Nota], summary="Listar notas")
def listar_notas(service: ServiceDep) -> list[Nota]:
    return service.listar()


@router.get("/curso/{curso_id}", response_model=list[Nota], summary="Notas por curso")
def listar_notas_por_curso(curso_id: int, service: ServiceDep) -> list[Nota]:
    return service.listar_por_curso(curso_id)


@router.get("/{nota_id}", response_model=Nota, summary="Obtener una nota")
def obtener_nota(nota_id: int, service: ServiceDep) -> Nota:
    return service.obtener(nota_id)


@router.post(
    "",
    response_model=Nota,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nota",
)
def crear_nota(datos: NotaCreate, service: ServiceDep) -> Nota:
    return service.crear(datos)


@router.put("/{nota_id}", response_model=Nota, summary="Actualizar una nota")
def actualizar_nota(nota_id: int, datos: NotaUpdate, service: ServiceDep) -> Nota:
    return service.actualizar(nota_id, datos)


@router.delete(
    "/{nota_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una nota",
)
def eliminar_nota(nota_id: int, service: ServiceDep) -> None:
    service.eliminar(nota_id)