from backend.schemas.notificaciones_schema import (
    Notificaciones,
    NotificacionesUpdate,
)


class NotificacionesRepository:
    def __init__(self) -> None:
        self._notificaciones = Notificaciones(
            evaluaciones=True,
            tareas=True,
            revisiones=True,
        )

    def obtener(self) -> Notificaciones:
        return self._notificaciones

    def actualizar(self, datos: NotificacionesUpdate) -> Notificaciones:
        self._notificaciones = Notificaciones(**datos.model_dump())
        return self._notificaciones


notificaciones_repository = NotificacionesRepository()
