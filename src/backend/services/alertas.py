from backend.repositories.alertas import AlertaRepository, alerta_repository
from backend.repositories.cursos import curso_repository
from backend.repositories.tareas import tarea_repository
from backend.schemas.alertas import Alerta, AlertaCreate
from backend.services.exceptions import ForbiddenError, NotFoundError


class AlertaService:
    def __init__(self, repository: AlertaRepository | None = None) -> None:
        self._repository = repository or alerta_repository

    def listar(self, id_usuario: int) -> list[Alerta]:
        return self._repository.listar_por_usuario(id_usuario)

    def crear(self, id_usuario: int, datos: AlertaCreate) -> Alerta:
        if datos.id_curso is not None and not curso_repository.pertenece_a_usuario(datos.id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        if datos.id_tarea is not None:
            tarea = tarea_repository.obtener(datos.id_tarea)
            if tarea is None or tarea.id_usuario != id_usuario:
                raise ForbiddenError("La tarea no pertenece al usuario.")
        return self._repository.agregar(id_usuario, datos)

    def marcar_leida(self, id_alerta: int, id_usuario: int) -> Alerta:
        alerta = self._repository.obtener(id_alerta)
        if alerta is None:
            raise NotFoundError(f"No existe la alerta {id_alerta}.")
        if alerta.id_usuario != id_usuario:
            raise ForbiddenError()
        result = self._repository.marcar_leida(id_alerta)
        if result is None:
            raise NotFoundError(f"No existe la alerta {id_alerta}.")
        return result

    def eliminar(self, id_alerta: int, id_usuario: int) -> None:
        alerta = self._repository.obtener(id_alerta)
        if alerta is None:
            raise NotFoundError(f"No existe la alerta {id_alerta}.")
        if alerta.id_usuario != id_usuario:
            raise ForbiddenError()
        self._repository.eliminar(id_alerta)


alerta_service = AlertaService()
