from typing import Annotated

from fastapi import APIRouter, Depends

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.dashboard import DashboardResumen
from backend.services.dashboard import DashboardService, dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
ServiceDep = Annotated[DashboardService, Depends(lambda: dashboard_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("/resumen", response_model=DashboardResumen)
def resumen(service: ServiceDep, user: UserDep) -> DashboardResumen:
    return service.resumen(user.id_usuario)
