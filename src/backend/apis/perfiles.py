from typing import Annotated

from fastapi import APIRouter, Depends

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.perfil import Perfil, PerfilUpdate
from backend.services.perfiles import PerfilService, perfil_service

router = APIRouter(prefix="/perfil", tags=["perfil"])
ServiceDep = Annotated[PerfilService, Depends(lambda: perfil_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("", response_model=Perfil)
def obtener(service: ServiceDep, user: UserDep) -> Perfil:
    return service.obtener(user.id_usuario)


@router.put("", response_model=Perfil)
def actualizar(datos: PerfilUpdate, service: ServiceDep, user: UserDep) -> Perfil:
    return service.actualizar(user.id_usuario, datos)
