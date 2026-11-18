from backend.repositories.perfiles import PerfilRepository, perfil_repository
from backend.schemas.perfil import Perfil, PerfilUpdate
from backend.services.exceptions import NotFoundError


class PerfilService:
    def __init__(self, repository: PerfilRepository | None = None) -> None:
        self._repository = repository or perfil_repository

    def obtener(self, id_usuario: int) -> Perfil:
        perfil = self._repository.get_by_usuario(id_usuario)
        if perfil is None:
            raise NotFoundError("Perfil no encontrado.")
        return perfil

    def actualizar(self, id_usuario: int, datos: PerfilUpdate) -> Perfil:
        perfil = self._repository.update(id_usuario, datos)
        if perfil is None:
            raise NotFoundError("Perfil no encontrado.")
        return perfil


perfil_service = PerfilService()
