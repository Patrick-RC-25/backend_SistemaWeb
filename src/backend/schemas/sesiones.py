from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SesionCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int | None = None
    id_tarea: int | None = None
    titulo: str = Field(..., min_length=2, max_length=120)
    fecha_inicio_programada: datetime
    fecha_fin_programada: datetime
    notas: str | None = Field(None, max_length=500)


class SesionUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int | None = None
    id_tarea: int | None = None
    titulo: str = Field(..., min_length=2, max_length=120)
    fecha_inicio_programada: datetime
    fecha_fin_programada: datetime
    notas: str | None = Field(None, max_length=500)
    estado: Literal["programada", "en_progreso", "completada", "cancelada"] = "programada"


class Sesion(BaseModel):
    id_sesion: int
    id_usuario: int
    id_curso: int | None = None
    id_tarea: int | None = None
    titulo: str
    fecha_inicio_programada: datetime
    fecha_fin_programada: datetime
    fecha_inicio_real: datetime | None = None
    fecha_fin_real: datetime | None = None
    estado: str
    notas: str | None = None
