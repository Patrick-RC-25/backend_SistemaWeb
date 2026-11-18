from backend.repositories.tareas import TareaRepository, tarea_repository
from backend.repositories.cursos import curso_repository
from backend.schemas.tareas import Tarea, TareaCreate, TareaUpdate
from backend.services.exceptions import ForbiddenError, NotFoundError


class TareaService:
    def __init__(self, repo: TareaRepository | None = None) -> None:
        self._repo = repo or tarea_repository

    def listar(self, id_usuario: int) -> list[Tarea]:
        return self._repo.listar(id_usuario)

    def crear(self, id_usuario: int, datos: TareaCreate) -> Tarea:
        if datos.id_curso is not None and not curso_repository.pertenece_a_usuario(datos.id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        return self._repo.agregar(id_usuario, datos)

    def actualizar(self, id_tarea: int, id_usuario: int, datos: TareaUpdate) -> Tarea:
        t = self._repo.obtener(id_tarea)
        if t is None:
            raise NotFoundError(f"No existe la tarea {id_tarea}.")
        if t.id_usuario != id_usuario:
            raise ForbiddenError()
        if datos.id_curso is not None and not curso_repository.pertenece_a_usuario(datos.id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        actualizada = self._repo.actualizar(id_tarea, datos)
        if actualizada is None:
            raise NotFoundError(f"No existe la tarea {id_tarea}.")
        return actualizada

    def eliminar(self, id_tarea: int, id_usuario: int) -> None:
        t = self._repo.obtener(id_tarea)
        if t is None:
            raise NotFoundError(f"No existe la tarea {id_tarea}.")
        if t.id_usuario != id_usuario:
            raise ForbiddenError()
        self._repo.eliminar(id_tarea)


tarea_service = TareaService()
