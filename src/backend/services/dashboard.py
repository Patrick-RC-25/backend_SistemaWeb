from backend.repositories.alertas import alerta_repository
from backend.repositories.cursos import curso_repository
from backend.repositories.objetivos import objetivo_repository
from backend.repositories.sesiones import sesion_repository
from backend.repositories.tareas import tarea_repository
from backend.schemas.dashboard import DashboardResumen


class DashboardService:
    def resumen(self, id_usuario: int) -> DashboardResumen:
        cursos = curso_repository.listar_por_usuario(id_usuario)
        tareas = tarea_repository.listar(id_usuario)
        sesiones_hoy = sesion_repository.listar_hoy(id_usuario)
        objetivos = objetivo_repository.listar(id_usuario)
        alertas = alerta_repository.listar_por_usuario(id_usuario)

        promedios = [c.promedio_actual for c in cursos if c.promedio_actual is not None]
        promedio_general = round(sum(promedios) / len(promedios), 2) if promedios else None

        tareas_pend = [t for t in tareas if t.estado in ("pendiente", "en_progreso")]
        objetivos_act = [o for o in objetivos if o.estado in ("pendiente", "en_progreso")]
        alertas_no_leidas = [a for a in alertas if not a.leida]

        necesita: list[str] = []
        for c in cursos:
            if c.promedio_actual is not None and c.nota_objetivo is not None:
                if c.promedio_actual < c.nota_objetivo:
                    necesita.append(
                        f"Curso «{c.nombre}»: promedio {c.promedio_actual} bajo objetivo {c.nota_objetivo}."
                    )
        for t in tareas_pend[:5]:
            if t.fecha_vencimiento is not None:
                necesita.append(f"Tarea pendiente «{t.titulo}» (prioridad {t.prioridad}).")
        for o in objetivos_act:
            if o.progreso < 50:
                necesita.append(f"Objetivo «{o.titulo}» con progreso {o.progreso}%.")

        return DashboardResumen(
            promedio_general=promedio_general,
            cursos_activos=len(cursos),
            tareas_pendientes=len(tareas_pend),
            alertas_no_leidas=len(alertas_no_leidas),
            objetivos_activos=len(objetivos_act),
            sesiones_hoy=len(sesiones_hoy),
            cursos=cursos,
            tareas_proximas=tareas_pend[:5],
            sesiones_hoy_lista=sesiones_hoy,
            objetivos=objetivos_act[:5],
            alertas_recientes=alertas_no_leidas[:5],
            necesita_atencion=necesita[:8],
        )


dashboard_service = DashboardService()
