from backend.repositories.notificaciones_repository import (
    NotificacionesRepository,
    notificaciones_repository,
)
from backend.schemas.notificaciones_schema import (
    Notificaciones,
    NotificacionesUpdate,
)


class NotificacionesService:
    def __init__(self, repository: NotificacionesRepository | None = None) -> None:
        self._repository = repository or notificaciones_repository

    def obtener(self) -> Notificaciones:
        return self._repository.obtener()

    def actualizar(self, datos: NotificacionesUpdate) -> Notificaciones:
        return self._repository.actualizar(datos)


notificaciones_service = NotificacionesService()
