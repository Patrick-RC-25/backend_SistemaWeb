from backend.repositories.alertas_repository import AlertaRepository, alerta_repository
from backend.schemas.alertas_schema import Alerta, AlertaCreate
from backend.services.exceptions import AlertaNotFoundError


class AlertaService:
    def __init__(self, repository: AlertaRepository | None = None) -> None:
        self._repository = repository or alerta_repository

    def listar(self) -> list[Alerta]:
        return self._repository.listar()

    def obtener(self, alerta_id: int) -> Alerta:
        alerta = self._repository.obtener(alerta_id)
        if alerta is None:
            raise AlertaNotFoundError(alerta_id)
        return alerta

    def crear(self, datos: AlertaCreate) -> Alerta:
        return self._repository.agregar(datos)

    def marcar_atendida(self, alerta_id: int) -> Alerta:
        alerta = self._repository.marcar_atendida(alerta_id)
        if alerta is None:
            raise AlertaNotFoundError(alerta_id)
        return alerta

    def eliminar(self, alerta_id: int) -> None:
        if not self._repository.eliminar(alerta_id):
            raise AlertaNotFoundError(alerta_id)


alerta_service = AlertaService()