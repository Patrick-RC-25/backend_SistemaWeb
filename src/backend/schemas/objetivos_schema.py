from pydantic import BaseModel, ConfigDict, Field


class Objetivo(BaseModel):
    """Objetivo académico almacenado."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: int
    titulo: str = Field(..., min_length=3, max_length=150)
    valor_actual: float = Field(..., ge=0, examples=[15.8])
    valor_meta: float = Field(..., ge=0, examples=[17.0])
    progreso: int = Field(..., ge=0, le=100, examples=[78])
    descripcion: str | None = Field(default=None, max_length=500)
