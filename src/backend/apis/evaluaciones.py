from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.apis.deps import get_current_user
from backend.schemas.auth import UsuarioResponse
from backend.schemas.evaluaciones import Evaluacion, EvaluacionCreate, EvaluacionUpdate
from backend.services.evaluaciones import EvaluacionService, evaluacion_service

router = APIRouter(prefix="/evaluaciones", tags=["evaluaciones"])
ServiceDep = Annotated[EvaluacionService, Depends(lambda: evaluacion_service)]
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("/curso/{id_curso}", response_model=list[Evaluacion])
def listar_por_curso(id_curso: int, service: ServiceDep, user: UserDep) -> list[Evaluacion]:
    return service.listar_por_curso(id_curso, user.id_usuario)


@router.post("", response_model=Evaluacion, status_code=status.HTTP_201_CREATED)
def crear(datos: EvaluacionCreate, service: ServiceDep, user: UserDep) -> Evaluacion:
    return service.crear(user.id_usuario, datos)


@router.put("/{id_evaluacion}", response_model=Evaluacion)
def actualizar(
    id_evaluacion: int, datos: EvaluacionUpdate, service: ServiceDep, user: UserDep
) -> Evaluacion:
    return service.actualizar(id_evaluacion, user.id_usuario, datos)


@router.delete("/{id_evaluacion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_evaluacion: int, service: ServiceDep, user: UserDep) -> None:
    service.eliminar(id_evaluacion, user.id_usuario)
