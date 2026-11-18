from backend.repositories.estudiante_repository import (
    EstudianteRepository,
    estudiante_repository,
)
from backend.schemas.estudiante_schema import Estudiante, EstudianteUpdate


class EstudianteService:
    def __init__(self, repository: EstudianteRepository | None = None) -> None:
        self._repository = repository or estudiante_repository

    def obtener(self) -> Estudiante:
        return self._repository.obtener()

    def actualizar(self, datos: EstudianteUpdate) -> Estudiante:
        return self._repository.actualizar(datos)


estudiante_service = EstudianteService()
