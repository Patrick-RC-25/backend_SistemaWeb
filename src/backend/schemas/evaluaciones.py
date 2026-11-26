from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EvaluacionCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int = Field(..., gt=0)
    id_tipo_evaluacion: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=120)
    ponderacion: Decimal = Field(..., ge=0, le=100, max_digits=5, decimal_places=2)
    nota_maxima: float = Field(default=20, ge=20, le=20)
    nota_obtenida: Decimal | None = Field(None, ge=0, le=20, max_digits=5, decimal_places=2)
    fecha_evaluacion: date | None = None

    @field_validator("nota_obtenida", mode="before")
    @classmethod
    def validar_precision_nota(cls, value):
        if isinstance(value, str) and "." in value and len(value.rsplit(".", 1)[1]) > 2:
            raise ValueError("La nota admite como máximo 2 decimales.")
        return value


class EvaluacionUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_tipo_evaluacion: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=120)
    ponderacion: Decimal = Field(..., ge=0, le=100, max_digits=5, decimal_places=2)
    nota_maxima: float = Field(..., ge=20, le=20)
    nota_obtenida: Decimal | None = Field(None, ge=0, le=20, max_digits=5, decimal_places=2)
    fecha_evaluacion: date | None = None

    @field_validator("nota_obtenida", mode="before")
    @classmethod
    def validar_precision_nota(cls, value):
        if isinstance(value, str) and "." in value and len(value.rsplit(".", 1)[1]) > 2:
            raise ValueError("La nota admite como máximo 2 decimales.")
        return value


class Evaluacion(BaseModel):
    id_evaluacion: int
    id_curso: int
    id_tipo_evaluacion: int
    nombre: str
    ponderacion: float
    nota_maxima: float
    nota_obtenida: Decimal | None = Field(None, ge=0, le=20, max_digits=5, decimal_places=2)
    fecha_evaluacion: date | None = None
