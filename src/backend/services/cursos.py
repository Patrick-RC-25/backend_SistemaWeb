from backend.repositories.cursos import CursoRepository, curso_repository
from backend.repositories.periodos import periodo_repository
from backend.schemas.cursos import Curso, CursoCreate, CursoUpdate
from backend.services.exceptions import ForbiddenError, NotFoundError


class CursoService:
    def __init__(self, repository: CursoRepository | None = None) -> None:
        self._repository = repository or curso_repository

    def listar(self, id_usuario: int) -> list[Curso]:
        return self._repository.listar_por_usuario(id_usuario)

    def obtener(self, id_curso: int, id_usuario: int) -> Curso:
        if not self._repository.pertenece_a_usuario(id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        curso = self._repository.obtener(id_curso)
        if curso is None:
            raise NotFoundError(f"No existe el curso {id_curso}.")
        return curso

    def crear(self, id_usuario: int, datos: CursoCreate) -> Curso:
        periodo = periodo_repository.obtener(datos.id_periodo)
        if periodo is None or periodo.id_usuario != id_usuario:
            raise ForbiddenError("El periodo no pertenece al usuario.")
        return self._repository.agregar(datos)

    def actualizar(self, id_curso: int, id_usuario: int, datos: CursoUpdate) -> Curso:
        if not self._repository.pertenece_a_usuario(id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        curso = self._repository.actualizar(id_curso, datos)
        if curso is None:
            raise NotFoundError(f"No existe el curso {id_curso}.")
        return curso

    def eliminar(self, id_curso: int, id_usuario: int) -> None:
        if not self._repository.pertenece_a_usuario(id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        if not self._repository.eliminar(id_curso):
            raise NotFoundError(f"No existe el curso {id_curso}.")


curso_service = CursoService()
