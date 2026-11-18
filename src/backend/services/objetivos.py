from backend.repositories.objetivos import ObjetivoRepository, objetivo_repository
from backend.repositories.cursos import curso_repository
from backend.schemas.objetivos import Objetivo, ObjetivoCreate, ObjetivoUpdate
from backend.services.exceptions import ForbiddenError, NotFoundError


class ObjetivoService:
    def __init__(self, repo: ObjetivoRepository | None = None) -> None:
        self._repo = repo or objetivo_repository

    def listar(self, id_usuario: int) -> list[Objetivo]:
        return self._repo.listar(id_usuario)

    def crear(self, id_usuario: int, datos: ObjetivoCreate) -> Objetivo:
        if datos.id_curso is not None and not curso_repository.pertenece_a_usuario(datos.id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        return self._repo.agregar(id_usuario, datos)

    def actualizar(self, id_objetivo: int, id_usuario: int, datos: ObjetivoUpdate) -> Objetivo:
        o = self._repo.obtener(id_objetivo)
        if o is None:
            raise NotFoundError(f"No existe el objetivo {id_objetivo}.")
        if o.id_usuario != id_usuario:
            raise ForbiddenError()
        if datos.id_curso is not None and not curso_repository.pertenece_a_usuario(datos.id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        actualizado = self._repo.actualizar(id_objetivo, datos)
        if actualizado is None:
            raise NotFoundError(f"No existe el objetivo {id_objetivo}.")
        return actualizado

    def eliminar(self, id_objetivo: int, id_usuario: int) -> None:
        o = self._repo.obtener(id_objetivo)
        if o is None:
            raise NotFoundError(f"No existe el objetivo {id_objetivo}.")
        if o.id_usuario != id_usuario:
            raise ForbiddenError()
        self._repo.eliminar(id_objetivo)


objetivo_service = ObjetivoService()
