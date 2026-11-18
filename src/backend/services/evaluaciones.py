from backend.repositories.cursos import curso_repository
from backend.repositories.evaluaciones import EvaluacionRepository, evaluacion_repository
from backend.schemas.evaluaciones import Evaluacion, EvaluacionCreate, EvaluacionUpdate
from backend.services.exceptions import BusinessRuleError, ForbiddenError, NotFoundError


class EvaluacionService:
    def __init__(self, repository: EvaluacionRepository | None = None) -> None:
        self._repository = repository or evaluacion_repository

    def listar_por_curso(self, id_curso: int, id_usuario: int) -> list[Evaluacion]:
        if not curso_repository.pertenece_a_usuario(id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        return self._repository.listar_por_curso(id_curso)

    def crear(self, id_usuario: int, datos: EvaluacionCreate) -> Evaluacion:
        if not curso_repository.pertenece_a_usuario(datos.id_curso, id_usuario):
            raise ForbiddenError("El curso no pertenece al usuario.")
        total = self._repository.ponderacion_total(datos.id_curso)
        if total + datos.ponderacion > 100.0001:
            raise BusinessRuleError(f"La suma de ponderaciones superaría el 100 % (actual: {total} %).")
        return self._repository.agregar(datos)

    def actualizar(
        self, id_evaluacion: int, id_usuario: int, datos: EvaluacionUpdate
    ) -> Evaluacion:
        ev = self._repository.obtener(id_evaluacion)
        if ev is None:
            raise NotFoundError(f"No existe la evaluación {id_evaluacion}.")
        if not curso_repository.pertenece_a_usuario(ev.id_curso, id_usuario):
            raise ForbiddenError("No autorizado.")
        total = self._repository.ponderacion_total(ev.id_curso, excluir_id=id_evaluacion)
        if total + datos.ponderacion > 100.0001:
            raise BusinessRuleError(f"La suma de ponderaciones superaría el 100 % (actual: {total} %).")
        actualizada = self._repository.actualizar(id_evaluacion, datos)
        if actualizada is None:
            raise NotFoundError(f"No existe la evaluación {id_evaluacion}.")
        return actualizada

    def eliminar(self, id_evaluacion: int, id_usuario: int) -> None:
        ev = self._repository.obtener(id_evaluacion)
        if ev is None:
            raise NotFoundError(f"No existe la evaluación {id_evaluacion}.")
        if not curso_repository.pertenece_a_usuario(ev.id_curso, id_usuario):
            raise ForbiddenError("No autorizado.")
        self._repository.eliminar(id_evaluacion)


evaluacion_service = EvaluacionService()
