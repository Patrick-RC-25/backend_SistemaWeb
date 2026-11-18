from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ObjetivoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int | None = None
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: str | None = Field(None, max_length=500)
    fecha_inicio: date
    fecha_limite: date | None = None
    progreso: float = Field(default=0, ge=0, le=100)


class ObjetivoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int | None = None
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: str | None = Field(None, max_length=500)
    fecha_inicio: date
    fecha_limite: date | None = None
    progreso: float = Field(..., ge=0, le=100)
    estado: Literal["pendiente", "en_progreso", "completado", "cancelado"] = "pendiente"


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
