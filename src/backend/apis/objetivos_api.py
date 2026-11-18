from typing import Annotated

from fastapi import APIRouter, Depends

from backend.schemas.objetivos_schema import Objetivo
from backend.services.objetivos_service import (
    ObjetivoService,
    objetivo_service,
)

router = APIRouter(prefix="/objetivos", tags=["objetivos"])


def get_objetivo_service() -> ObjetivoService:
    return objetivo_service


ServiceDep = Annotated[ObjetivoService, Depends(get_objetivo_service)]


@router.get("", response_model=list[Objetivo], summary="Listar objetivos")
def listar_objetivos(service: ServiceDep) -> list[Objetivo]:
    return service.listar()
