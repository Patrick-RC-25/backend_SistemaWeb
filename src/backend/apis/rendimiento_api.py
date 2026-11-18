from typing import Annotated

from fastapi import APIRouter, Depends

from backend.schemas.rendimiento_schema import Rendimiento
from backend.services.rendimiento_service import (
    RendimientoService,
    rendimiento_service,
)

router = APIRouter(prefix="/rendimiento", tags=["rendimiento"])


def get_rendimiento_service() -> RendimientoService:
    return rendimiento_service


ServiceDep = Annotated[RendimientoService, Depends(get_rendimiento_service)]


@router.get("", response_model=Rendimiento, summary="Obtener el rendimiento")
def obtener_rendimiento(service: ServiceDep) -> Rendimiento:
    return service.obtener()
