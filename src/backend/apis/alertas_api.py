from typing import Annotated
from fastapi import APIRouter, Depends, status
from backend.schemas.alertas_schema import Alerta, AlertaCreate
from backend.services.alertas_service import AlertaService, alerta_service

router = APIRouter(prefix="/alertas", tags=["alertas"])


def get_alerta_service() -> AlertaService:
    return alerta_service


ServiceDep = Annotated[AlertaService, Depends(get_alerta_service)]


@router.get("", response_model=list[Alerta], summary="Listar alertas")
def listar_alertas(service: ServiceDep) -> list[Alerta]:
    return service.listar()


@router.get("/{alerta_id}", response_model=Alerta, summary="Obtener una alerta")
def obtener_alerta(alerta_id: int, service: ServiceDep) -> Alerta:
    return service.obtener(alerta_id)


@router.post(
    "",
    response_model=Alerta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una alerta",
)
def crear_alerta(datos: AlertaCreate, service: ServiceDep) -> Alerta:
    return service.crear(datos)


@router.patch(
    "/{alerta_id}/atendida",
    response_model=Alerta,
    summary="Marcar alerta como atendida",
)
def marcar_alerta_atendida(alerta_id: int, service: ServiceDep) -> Alerta:
    return service.marcar_atendida(alerta_id)


@router.delete(
    "/{alerta_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una alerta",
)
def eliminar_alerta(alerta_id: int, service: ServiceDep) -> None:
    service.eliminar(alerta_id)