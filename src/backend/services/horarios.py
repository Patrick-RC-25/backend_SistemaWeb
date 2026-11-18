from backend.repositories.cursos import curso_repository
from backend.repositories.horarios import HorarioRepository, horario_repository
from backend.schemas.horarios import Horario, HorarioCreate, HorarioUpdate
from backend.services.exceptions import ForbiddenError, NotFoundError


class HorarioService:
    def __init__(self, repo: HorarioRepository | None = None) -> None:
        self._repo = repo or horario_repository

    def listar_usuario(self, id_usuario: int) -> list[Horario]:
        return self._repo.listar_por_usuario(id_usuario)

    def listar_curso(self, id_curso: int, id_usuario: int) -> list[Horario]:
        if not curso_repository.pertenece_a_usuario(id_curso, id_usuario):
            raise ForbiddenError()
        return self._repo.listar_por_curso(id_curso)

    def crear(self, id_usuario: int, datos: HorarioCreate) -> Horario:
        if not curso_repository.pertenece_a_usuario(datos.id_curso, id_usuario):
            raise ForbiddenError()
        return self._repo.agregar(datos)

    def actualizar(self, id_horario: int, id_usuario: int, datos: HorarioUpdate) -> Horario:
        h = self._repo.obtener(id_horario)
        if h is None:
            raise NotFoundError(f"No existe el horario {id_horario}.")
        if not curso_repository.pertenece_a_usuario(h.id_curso, id_usuario):
            raise ForbiddenError()
        actualizado = self._repo.actualizar(id_horario, datos)
        if actualizado is None:
            raise NotFoundError(f"No existe el horario {id_horario}.")
        return actualizado

    def eliminar(self, id_horario: int, id_usuario: int) -> None:
        h = self._repo.obtener(id_horario)
        if h is None:
            raise NotFoundError(f"No existe el horario {id_horario}.")
        if not curso_repository.pertenece_a_usuario(h.id_curso, id_usuario):
            raise ForbiddenError()
        self._repo.eliminar(id_horario)


horario_service = HorarioService()
