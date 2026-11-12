from backend.repositories.cursos_repository import curso_repository
from backend.repositories.notas_repository import NotaRepository, nota_repository
from backend.schemas.notas_schema import Nota, NotaCreate, NotaUpdate
from backend.services.exceptions import CursoInvalidoError, NotaNotFoundError


class NotaService:
    def __init__(self, repository: NotaRepository | None = None) -> None:
        self._repository = repository or nota_repository

    def listar(self) -> list[Nota]:
        return self._repository.listar()

    def obtener(self, nota_id: int) -> Nota:
        nota = self._repository.obtener(nota_id)
        if nota is None:
            raise NotaNotFoundError(nota_id)
        return nota

    def listar_por_curso(self, curso_id: int) -> list[Nota]:
        if not curso_repository.existe(curso_id):
            raise CursoInvalidoError(curso_id)
        return self._repository.listar_por_curso(curso_id)

    def crear(self, datos: NotaCreate) -> Nota:
        if not curso_repository.existe(datos.curso_id):
            raise CursoInvalidoError(datos.curso_id)
        return self._repository.agregar(datos)

    def actualizar(self, nota_id: int, datos: NotaUpdate) -> Nota:
        if not curso_repository.existe(datos.curso_id):
            raise CursoInvalidoError(datos.curso_id)
        nota = self._repository.actualizar(nota_id, datos)
        if nota is None:
            raise NotaNotFoundError(nota_id)
        return nota

    def eliminar(self, nota_id: int) -> None:
        if not self._repository.eliminar(nota_id):
            raise NotaNotFoundError(nota_id)


nota_service = NotaService()