from pydantic import BaseModel, ConfigDict, Field


class CursoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_periodo: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=120)
    codigo: str | None = Field(None, max_length=30)
    docente: str | None = Field(None, max_length=120)
    creditos: int | None = Field(None, gt=0, le=20)
    color: str | None = Field(None, max_length=20)
    nota_objetivo: float | None = Field(None, ge=0, le=20)


class CursoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(..., min_length=2, max_length=120)
    codigo: str | None = Field(None, max_length=30)
    docente: str | None = Field(None, max_length=120)
    creditos: int | None = Field(None, gt=0, le=20)
    color: str | None = Field(None, max_length=20)
    nota_objetivo: float | None = Field(None, ge=0, le=20)
    estado: bool = True


class Curso(BaseModel):
    id_curso: int
    id_periodo: int
    nombre: str
    codigo: str | None = None
    docente: str | None = None
    creditos: int | None = None
    color: str | None = None
    nota_objetivo: float | None = None
    estado: bool = True
    promedio_actual: float | None = None
