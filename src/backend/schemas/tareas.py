from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TareaCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int | None = None
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: str | None = Field(None, max_length=500)
    fecha_vencimiento: datetime | None = None
    prioridad: Literal["baja", "media", "alta"] = "media"
    estado: Literal["pendiente", "en_progreso", "completada", "cancelada"] = "pendiente"


class TareaUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int | None = None
    titulo: str = Field(..., min_length=2, max_length=150)
    descripcion: str | None = Field(None, max_length=500)
    fecha_vencimiento: datetime | None = None
    prioridad: Literal["baja", "media", "alta"] = "media"
    estado: Literal["pendiente", "en_progreso", "completada", "cancelada"] = "pendiente"


class Tarea(BaseModel):
    id_tarea: int
    id_usuario: int
    id_curso: int | None = None
    titulo: str
    descripcion: str | None = None
    fecha_vencimiento: datetime | None = None
    prioridad: str
    estado: str
    fecha_completada: datetime | None = None
