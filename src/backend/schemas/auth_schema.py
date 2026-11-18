from pydantic import BaseModel, ConfigDict, Field

from backend.schemas.estudiante_schema import Estudiante


class LoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: str = Field(
        ..., min_length=5, max_length=150, examples=["demo@carlito.app"]
    )
    password: str = Field(..., min_length=4, max_length=100, examples=["demo"])


class LoginResponse(BaseModel):
    autenticado: bool
    estudiante: Estudiante
