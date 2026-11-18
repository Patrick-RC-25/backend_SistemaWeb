from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class PeriodoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(..., min_length=2, max_length=100)
    fecha_inicio: date
    fecha_fin: date
    estado: str = Field(default="activo", pattern=r"^(activo|finalizado|planificado)$")


class Periodo(PeriodoCreate):
    id_periodo: int
    id_usuario: int
