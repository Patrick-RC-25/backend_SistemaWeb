from pydantic import BaseModel, ConfigDict, Field


class CursoBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(..., min_length=2, max_length=120, examples=["Sistemas Operativos"])
    codigo: str = Field(..., min_length=2, max_length=20, examples=["SIS-230"])
    creditos: int = Field(..., gt=0, le=10, examples=[4])
    promedio: float = Field(..., ge=0, le=20, examples=[13.8])
    docente: str = Field(..., min_length=2, max_length=100, examples=["Dr. Pedro Vargas"])


class CursoCreate(CursoBase):
    """Datos para crear un curso."""


class CursoUpdate(BaseModel):
    """Datos modificables de un curso (el id no se puede cambiar)."""

    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(..., min_length=2, max_length=120)
    codigo: str = Field(..., min_length=2, max_length=20)
    creditos: int = Field(..., gt=0, le=10)
    promedio: float = Field(..., ge=0, le=20)
    docente: str = Field(..., min_length=2, max_length=100)


class Curso(CursoBase):
    """Curso almacenado."""

    id: int
