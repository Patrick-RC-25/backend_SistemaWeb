from backend.repositories.sesiones import SesionRepository, sesion_repository
from backend.repositories.cursos import curso_repository
from backend.repositories.tareas import tarea_repository
from backend.schemas.sesiones import Sesion, SesionCreate, SesionUpdate
from backend.services.exceptions import ForbiddenError, NotFoundError


class SesionService:
    def __init__(self, repo: SesionRepository | None = None) -> None:
        self._repo = repo or sesion_repository

    def listar(self, id_usuario: int) -> list[Sesion]:
        return self._repo.listar(id_usuario)

    def listar_hoy(self, id_usuario: int) -> list[Sesion]:
        return self._repo.listar_hoy(id_usuario)

    def _validar_relaciones(self, id_usuario: int, id_curso: int | None, id_tarea: int | None) -> None:
        if id_curso is not None and not curso_repository.pertenece_a_usuario(id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        if id_tarea is not None:
            tarea = tarea_repository.obtener(id_tarea)
            if tarea is None or tarea.id_usuario != id_usuario:
                raise ForbiddenError("La tarea no pertenece al usuario.")

    def crear(self, id_usuario: int, datos: SesionCreate) -> Sesion:
        self._validar_relaciones(id_usuario, datos.id_curso, datos.id_tarea)
        return self._repo.agregar(id_usuario, datos)

    def actualizar(self, id_sesion: int, id_usuario: int, datos: SesionUpdate) -> Sesion:
        s = self._repo.obtener(id_sesion)
        if s is None:
            raise NotFoundError(f"No existe la sesión {id_sesion}.")
        if s.id_usuario != id_usuario:
            raise ForbiddenError()
        self._validar_relaciones(id_usuario, datos.id_curso, datos.id_tarea)
        actualizada = self._repo.actualizar(id_sesion, datos)
        if actualizada is None:
            raise NotFoundError(f"No existe la sesión {id_sesion}.")
        return actualizada

    def iniciar(self, id_sesion: int, id_usuario: int) -> Sesion:
        s = self._repo.obtener(id_sesion)
        if s is None:
            raise NotFoundError(f"No existe la sesión {id_sesion}.")
        if s.id_usuario != id_usuario:
            raise ForbiddenError()
        result = self._repo.iniciar(id_sesion)
        if result is None:
            raise NotFoundError("No se pudo iniciar la sesión.")
        return result

    def finalizar(self, id_sesion: int, id_usuario: int) -> Sesion:
        s = self._repo.obtener(id_sesion)
        if s is None:
            raise NotFoundError(f"No existe la sesión {id_sesion}.")
        if s.id_usuario != id_usuario:
            raise ForbiddenError()
        result = self._repo.finalizar(id_sesion)
        if result is None:
            raise NotFoundError("No se pudo finalizar la sesión.")
        return result

    def cancelar(self, id_sesion: int, id_usuario: int) -> Sesion:
        s = self._repo.obtener(id_sesion)
        if s is None:
            raise NotFoundError(f"No existe la sesión {id_sesion}.")
        if s.id_usuario != id_usuario:
            raise ForbiddenError()
        result = self._repo.cancelar(id_sesion)
        if result is None:
            raise NotFoundError("No se pudo cancelar la sesión.")
        return result

    def eliminar(self, id_sesion: int, id_usuario: int) -> None:
        s = self._repo.obtener(id_sesion)
        if s is None:
            raise NotFoundError(f"No existe la sesión {id_sesion}.")
        if s.id_usuario != id_usuario:
            raise ForbiddenError()
        self._repo.eliminar(id_sesion)


sesion_service = SesionService()
