from backend.repositories.cursos_repository import curso_repository
from backend.repositories.sesiones_repository import (
    SesionRepository,
    sesion_repository,
)
from backend.schemas.sesiones_schema import Sesion, SesionCreate
from backend.services.exceptions import CursoInvalidoError, SesionNotFoundError


class SesionService:
    def __init__(self, repository: SesionRepository | None = None) -> None:
        self._repository = repository or sesion_repository

    def listar(self) -> list[Sesion]:
        return self._repository.listar()

    def crear(self, datos: SesionCreate) -> Sesion:
        curso = curso_repository.obtener(datos.curso_id)
        if curso is None:
            raise CursoInvalidoError(datos.curso_id)
        return self._repository.agregar(datos, curso.nombre)

    def completar(self, sesion_id: int) -> Sesion:
        sesion = self._repository.actualizar_estado(sesion_id, "completada")
        if sesion is None:
            raise SesionNotFoundError(sesion_id)
        return sesion

    def cancelar(self, sesion_id: int) -> Sesion:
        sesion = self._repository.actualizar_estado(sesion_id, "cancelada")
        if sesion is None:
            raise SesionNotFoundError(sesion_id)
        return sesion


sesion_service = SesionService()
