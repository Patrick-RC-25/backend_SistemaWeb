from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class NotaBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    curso_id: int = Field(..., gt=0, examples=[1])
    nombre: str = Field(..., min_length=2, max_length=100, examples=["Parcial 1"])
    puntaje: float = Field(..., ge=0, le=20, examples=[14.5])
    peso: float = Field(..., gt=0, le=100, examples=[25])
    fecha: str = Field(..., min_length=8, max_length=20, examples=["2026-10-10"])
    tipo: Literal["examen", "tarea", "quiz", "proyecto"] = Field(
        ..., examples=["examen"]
    )


class NotaCreate(NotaBase):
    """Datos para crear una nota."""


class NotaUpdate(BaseModel):
    """Datos modificables de una nota (el id no se puede cambiar)."""

    model_config = ConfigDict(str_strip_whitespace=True)

    curso_id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=100)
    puntaje: float = Field(..., ge=0, le=20)
    peso: float = Field(..., gt=0, le=100)
    fecha: str = Field(..., min_length=8, max_length=20)
    tipo: Literal["examen", "tarea", "quiz", "proyecto"]


class Nota(NotaBase):
    """Nota almacenada."""

    id: int