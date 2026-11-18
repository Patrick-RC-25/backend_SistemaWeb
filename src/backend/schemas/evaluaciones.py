from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class EvaluacionCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_curso: int = Field(..., gt=0)
    id_tipo_evaluacion: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=120)
    ponderacion: float = Field(..., ge=0, le=100)
    nota_maxima: float = Field(default=20, ge=20, le=20)
    nota_obtenida: float | None = Field(None, ge=0, le=20)
    fecha_evaluacion: date | None = None


class EvaluacionUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_tipo_evaluacion: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=120)
    ponderacion: float = Field(..., ge=0, le=100)
    nota_maxima: float = Field(..., ge=20, le=20)
    nota_obtenida: float | None = Field(None, ge=0, le=20)
    fecha_evaluacion: date | None = None


class Evaluacion(BaseModel):
    id_evaluacion: int
    id_curso: int
    id_tipo_evaluacion: int
    nombre: str
    ponderacion: float
    nota_maxima: float
    nota_obtenida: float | None = Field(None, ge=0, le=20)
    fecha_evaluacion: date | None = None
