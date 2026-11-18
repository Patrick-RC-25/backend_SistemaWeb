from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.periodos import Periodo, PeriodoCreate
from backend.services.periodos import PeriodoService, periodo_service

router = APIRouter(prefix="/periodos", tags=["periodos"])
ServiceDep = Annotated[PeriodoService, Depends(lambda: periodo_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("", response_model=list[Periodo])
def listar(service: ServiceDep, user: UserDep) -> list[Periodo]:
    return service.listar(user.id_usuario)


@router.post("", response_model=Periodo, status_code=status.HTTP_201_CREATED)
def crear(datos: PeriodoCreate, service: ServiceDep, user: UserDep) -> Periodo:
    return service.crear(user.id_usuario, datos)


@router.get("/{id_periodo}", response_model=Periodo)
def obtener(id_periodo: int, service: ServiceDep, user: UserDep) -> Periodo:
    return service.obtener(id_periodo, user.id_usuario)
