from pydantic import BaseModel


class Notificaciones(BaseModel):
    """Preferencias de notificación del estudiante."""

    evaluaciones: bool = True
    tareas: bool = True
    revisiones: bool = True


class NotificacionesUpdate(Notificaciones):
    """Datos modificables de las preferencias de notificación."""
