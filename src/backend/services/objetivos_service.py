from backend.repositories.objetivos_repository import (
    ObjetivoRepository,
    objetivo_repository,
)
from backend.schemas.objetivos_schema import Objetivo


class ObjetivoService:
    def __init__(self, repository: ObjetivoRepository | None = None) -> None:
        self._repository = repository or objetivo_repository

    def listar(self) -> list[Objetivo]:
        return self._repository.listar()


objetivo_service = ObjetivoService()
