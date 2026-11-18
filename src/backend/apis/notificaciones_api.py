from typing import Annotated

from fastapi import APIRouter, Depends

from backend.schemas.notificaciones_schema import (
    Notificaciones,
    NotificacionesUpdate,
)
from backend.services.notificaciones_service import (
    NotificacionesService,
    notificaciones_service,
)

router = APIRouter(prefix="/notificaciones", tags=["notificaciones"])


def get_notificaciones_service() -> NotificacionesService:
    return notificaciones_service


ServiceDep = Annotated[
    NotificacionesService, Depends(get_notificaciones_service)
]


@router.get(
    "",
    response_model=Notificaciones,
    summary="Obtener preferencias de notificación",
)
def obtener_notificaciones(service: ServiceDep) -> Notificaciones:
    return service.obtener()


@router.put(
    "",
    response_model=Notificaciones,
    summary="Actualizar preferencias de notificación",
)
def actualizar_notificaciones(
    datos: NotificacionesUpdate, service: ServiceDep
) -> Notificaciones:
    return service.actualizar(datos)
