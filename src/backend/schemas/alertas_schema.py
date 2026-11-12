from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AlertaBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    tipo: Literal["evaluacion", "tarea", "revision"] = Field(..., examples=["evaluacion"])
    prioridad: Literal["urgente", "importante", "sugerencia"] = Field(
        ..., examples=["urgente"]
    )
    titulo: str = Field(..., min_length=3, max_length=150)
    curso_nombre: str = Field(..., min_length=2, max_length=120)
    fecha: str = Field(..., min_length=3, max_length=80)
    detalle: str = Field(..., min_length=5, max_length=500)
    atendida: bool = False


class AlertaCreate(AlertaBase):
    """Datos para crear una alerta."""


class Alerta(AlertaBase):
    """Alerta almacenada."""

    id: int