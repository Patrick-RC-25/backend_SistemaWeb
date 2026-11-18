from backend.schemas.objetivos_schema import Objetivo


class ObjetivoRepository:
    def __init__(self) -> None:
        self._objetivos: dict[int, Objetivo] = {
            1: Objetivo(
                id=1,
                titulo="Promedio general del semestre",
                valor_actual=15.8,
                valor_meta=17.0,
                progreso=78,
                descripcion=(
                    "Meta personal para mantener beca de excelencia en la "
                    "Universidad Peruana Unión - Huancayo."
                ),
            ),
            2: Objetivo(
                id=2,
                titulo="Cursos aprobados sin aplazos",
                valor_actual=5,
                valor_meta=6,
                progreso=83,
                descripcion="Aprobar todos los cursos del ciclo sin recuperación.",
            ),
        }

    def listar(self) -> list[Objetivo]:
        return list(self._objetivos.values())

    def obtener(self, objetivo_id: int) -> Objetivo | None:
        return self._objetivos.get(objetivo_id)


objetivo_repository = ObjetivoRepository()
