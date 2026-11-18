from typing import Annotated

from fastapi import APIRouter, Depends

from backend.schemas.estudiante_schema import Estudiante, EstudianteUpdate
from backend.services.estudiante_service import (
    EstudianteService,
    estudiante_service,
)

router = APIRouter(prefix="/estudiante", tags=["estudiante"])


def get_estudiante_service() -> EstudianteService:
    return estudiante_service


ServiceDep = Annotated[EstudianteService, Depends(get_estudiante_service)]


@router.get("", response_model=Estudiante, summary="Obtener el estudiante")
def obtener_estudiante(service: ServiceDep) -> Estudiante:
    return service.obtener()


@router.put("", response_model=Estudiante, summary="Actualizar el estudiante")
def actualizar_estudiante(
    datos: EstudianteUpdate, service: ServiceDep
) -> Estudiante:
    return service.actualizar(datos)
