from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ObjetivoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int | None = None
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: str | None = Field(None, max_length=500)
    fecha_inicio: date
    fecha_limite: date | None = None


class ObjetivoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int | None = None
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: str | None = Field(None, max_length=500)
    fecha_inicio: date
    fecha_limite: date | None = None


class Objetivo(BaseModel):
    id_objetivo: int
    id_usuario: int
    id_curso: int | None = None
    titulo: str
    descripcion: str | None = None
    fecha_inicio: date
    fecha_limite: date | None = None
    progreso: float
    estado: str
    total_tareas: int = 0
    tareas_completadas: int = 0
