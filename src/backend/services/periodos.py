from backend.repositories.periodos import PeriodoRepository, periodo_repository
from backend.schemas.periodos import Periodo, PeriodoCreate
from backend.services.exceptions import ForbiddenError, NotFoundError


class PeriodoService:
    def __init__(self, repository: PeriodoRepository | None = None) -> None:
        self._repository = repository or periodo_repository

    def listar(self, id_usuario: int) -> list[Periodo]:
        return self._repository.listar_por_usuario(id_usuario)

    def crear(self, id_usuario: int, datos: PeriodoCreate) -> Periodo:
        return self._repository.create(id_usuario, datos)

    def obtener(self, id_periodo: int, id_usuario: int) -> Periodo:
        periodo = self._repository.obtener(id_periodo)
        if periodo is None:
            raise NotFoundError(f"No existe el periodo {id_periodo}.")
        if periodo.id_usuario != id_usuario:
            raise ForbiddenError()
        return periodo


periodo_service = PeriodoService()
