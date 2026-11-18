from pydantic import BaseModel, ConfigDict, Field


class PerfilUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    universidad: str | None = Field(None, max_length=150)
    carrera: str | None = Field(None, max_length=150)
    ciclo: str | None = Field(None, max_length=30)
    foto_url: str | None = Field(None, max_length=300)


class Perfil(BaseModel):
    id_perfil: int
    id_usuario: int
    nombres: str
    apellidos: str
    universidad: str | None = None
    carrera: str | None = None
    ciclo: str | None = None
    foto_url: str | None = None
