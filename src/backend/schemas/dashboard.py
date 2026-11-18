from pydantic import BaseModel

from backend.schemas.alertas import Alerta
from backend.schemas.cursos import Curso
from backend.schemas.objetivos import Objetivo
from backend.schemas.sesiones import Sesion
from backend.schemas.tareas import Tarea


class DashboardResumen(BaseModel):
    promedio_general: float | None
    cursos_activos: int
    tareas_pendientes: int
    alertas_no_leidas: int
    objetivos_activos: int
    sesiones_hoy: int
    cursos: list[Curso]
    tareas_proximas: list[Tarea]
    sesiones_hoy_lista: list[Sesion]
    objetivos: list[Objetivo]
    alertas_recientes: list[Alerta]
    necesita_atencion: list[str]
