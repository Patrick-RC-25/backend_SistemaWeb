from pydantic import BaseModel, Field


class PuntoSemanal(BaseModel):
    semana: str = Field(..., min_length=3, max_length=20, examples=["Sem 1"])
    promedio: float = Field(..., ge=0, le=20, examples=[14.6])
    meta: float = Field(..., ge=0, le=20, examples=[17.0])


class CursoRendimiento(BaseModel):
    curso_id: int
    curso_nombre: str
    promedio: float = Field(..., ge=0, le=20)
    variacion: float
    progreso: int = Field(..., ge=0, le=100)


class Rendimiento(BaseModel):
    promedio_general: float = Field(..., ge=0, le=20)
    promedio_meta: float = Field(..., ge=0, le=20)
    promedio_inicial: float = Field(..., ge=0, le=20)
    historial_semanal: list[PuntoSemanal]
    cursos: list[CursoRendimiento]
