from backend.repositories.cursos_repository import (
    CursoRepository,
    curso_repository,
)
from backend.repositories.objetivos_repository import (
    ObjetivoRepository,
    objetivo_repository,
)
from backend.schemas.cursos_schema import Curso
from backend.schemas.rendimiento_schema import (
    CursoRendimiento,
    PuntoSemanal,
    Rendimiento,
)

# Historial de demostración para conservar la gráfica del frontend.
HISTORIAL_SEMANAL = [
    PuntoSemanal(semana="Sem 1", promedio=14.6, meta=17),
    PuntoSemanal(semana="Sem 2", promedio=15.0, meta=17),
    PuntoSemanal(semana="Sem 3", promedio=15.3, meta=17),
    PuntoSemanal(semana="Sem 4", promedio=15.1, meta=17),
    PuntoSemanal(semana="Sem 5", promedio=15.6, meta=17),
    PuntoSemanal(semana="Sem 6", promedio=15.8, meta=17),
]


class RendimientoService:
    def __init__(
        self,
        cursos: CursoRepository | None = None,
        objetivos: ObjetivoRepository | None = None,
    ) -> None:
        self._cursos = cursos or curso_repository
        self._objetivos = objetivos or objetivo_repository

    def obtener(self) -> Rendimiento:
        cursos = self._cursos.listar()
        objetivos = self._objetivos.listar()
        promedio_meta = objetivos[0].valor_meta if objetivos else 20.0
        return Rendimiento(
            promedio_general=round(self._promedio_general(cursos), 1),
            promedio_meta=promedio_meta,
            promedio_inicial=HISTORIAL_SEMANAL[0].promedio,
            historial_semanal=HISTORIAL_SEMANAL,
            cursos=[self._curso_rendimiento(curso) for curso in cursos],
        )

    @staticmethod
    def _promedio_general(cursos: list[Curso]) -> float:
        creditos = sum(curso.creditos for curso in cursos)
        if creditos == 0:
            return 0.0
        total = sum(curso.promedio * curso.creditos for curso in cursos)
        return total / creditos

    @staticmethod
    def _curso_rendimiento(curso: Curso) -> CursoRendimiento:
        return CursoRendimiento(
            curso_id=curso.id,
            curso_nombre=curso.nombre,
            promedio=curso.promedio,
            variacion=round(curso.promedio - curso.promedio_anterior, 1),
            progreso=min(100, round((curso.promedio / 20) * 100)),
        )


rendimiento_service = RendimientoService()
