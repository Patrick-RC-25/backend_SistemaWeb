from pydantic import BaseModel, ConfigDict, Field, field_validator


class UsuarioRegistro(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    contrasena: str = Field(..., min_length=8, max_length=100)
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    universidad: str | None = Field(None, max_length=150)
    carrera: str | None = Field(None, max_length=150)
    ciclo: str | None = Field(None, max_length=30)

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v: str) -> str:
        return v.strip().lower()


class UsuarioLogin(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: str
    contrasena: str

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v: str) -> str:
        return v.strip().lower()


class UsuarioResponse(BaseModel):
    id_usuario: int
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str
    id_usuario: int
