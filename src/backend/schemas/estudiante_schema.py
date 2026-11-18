from pydantic import BaseModel, ConfigDict, Field


class EstudianteBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombres: str = Field(..., min_length=2, max_length=100, examples=["Carlos"])
    apellidos: str = Field(
        ..., min_length=2, max_length=100, examples=["Mendoza Rojas"]
    )
    correo: str = Field(
        ..., min_length=5, max_length=150, examples=["carlos.mendoza@upeu.edu.pe"]
    )
    carrera: str = Field(
        ..., min_length=2, max_length=120, examples=["Ingeniería de Sistemas"]
    )
    semestre: int = Field(..., ge=1, le=12, examples=[6])


class EstudianteUpdate(EstudianteBase):
    """Datos modificables del estudiante."""


class Estudiante(EstudianteBase):
    """Estudiante almacenado."""

    id: int
    iniciales: str = Field(..., min_length=1, max_length=4, examples=["CM"])
    avatar_url: str | None = None
