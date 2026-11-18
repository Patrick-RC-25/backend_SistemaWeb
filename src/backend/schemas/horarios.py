from datetime import time

from pydantic import BaseModel, ConfigDict, Field


class HorarioCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int = Field(..., gt=0)
    dia_semana: int = Field(..., ge=1, le=7)
    hora_inicio: time
    hora_fin: time
    aula: str | None = Field(None, max_length=50)


class HorarioUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    dia_semana: int = Field(..., ge=1, le=7)
    hora_inicio: time
    hora_fin: time
    aula: str | None = Field(None, max_length=50)


class Horario(BaseModel):
    id_horario: int
    id_curso: int
    dia_semana: int
    hora_inicio: time
    hora_fin: time
    aula: str | None = None
