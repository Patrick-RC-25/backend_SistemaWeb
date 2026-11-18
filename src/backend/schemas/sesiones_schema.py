from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SesionBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    curso_id: int = Field(..., gt=0, examples=[4])
    titulo: str = Field(..., min_length=3, max_length=150)
    descripcion: str = Field(default="", max_length=500)
    fecha: str = Field(..., min_length=8, max_length=20, examples=["2026-11-12"])
    hora_inicio: str = Field(..., min_length=4, max_length=5, examples=["07:00"])
    duracion_minutos: int = Field(..., gt=0, le=480, examples=[90])


class SesionCreate(SesionBase):
    """Datos para crear una sesión de estudio."""


class Sesion(SesionBase):
    """Sesión de estudio almacenada."""

    id: int
    curso_nombre: str = Field(..., min_length=2, max_length=120)
    estado: Literal["pendiente", "completada", "cancelada"] = "pendiente"
