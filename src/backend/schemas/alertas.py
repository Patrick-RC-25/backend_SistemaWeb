from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AlertaCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int | None = None
    id_tarea: int | None = None
    id_tipo_alerta: int = Field(..., gt=0)
    titulo: str = Field(..., min_length=2, max_length=120)
    mensaje: str = Field(..., min_length=2, max_length=500)
    fecha_programada: datetime | None = None


class Alerta(BaseModel):
    id_alerta: int
    id_usuario: int
    id_curso: int | None = None
    id_tarea: int | None = None
    id_tipo_alerta: int
    titulo: str
    mensaje: str
    fecha_programada: datetime | None = None
    leida: bool = False
