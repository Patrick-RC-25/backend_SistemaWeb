from pydantic import BaseModel


class CursoRendimiento(BaseModel):
    id_curso: int
    nombre: str
    promedio: float | None
    nota_objetivo: float | None
    diferencia: float | None


class RendimientoResumen(BaseModel):
    promedio_general: float | None
    cursos: list[CursoRendimiento]
    cursos_bajo_objetivo: list[str]
    recomendaciones: list[str]
