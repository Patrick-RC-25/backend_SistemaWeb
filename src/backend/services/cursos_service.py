from backend.repositories.cursos_repository import CursoRepository, curso_repository
from backend.schemas.cursos_schema import Curso, CursoCreate, CursoUpdate
from backend.services.exceptions import CursoNotFoundError


class CursoService:
    def __init__(self, repository: CursoRepository | None = None) -> None:
        self._repository = repository or curso_repository

    def listar(self) -> list[Curso]:
        return self._repository.listar()

    def obtener(self, curso_id: int) -> Curso:
        curso = self._repository.obtener(curso_id)
        if curso is None:
            raise CursoNotFoundError(curso_id)
        return curso

    def crear(self, datos: CursoCreate) -> Curso:
        return self._repository.agregar(datos)

    def actualizar(self, curso_id: int, datos: CursoUpdate) -> Curso:
        curso = self._repository.actualizar(curso_id, datos)
        if curso is None:
            raise CursoNotFoundError(curso_id)
        return curso

    def eliminar(self, curso_id: int) -> None:
        if not self._repository.eliminar(curso_id):
            raise CursoNotFoundError(curso_id)


curso_service = CursoService()