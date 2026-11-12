from backend.schemas.notas_schema import Nota, NotaCreate, NotaUpdate


class NotaRepository:
    def __init__(self) -> None:
        self._notas: dict[int, Nota] = {
            1: Nota(
                id=1,
                curso_id=1,
                nombre="Práctica 1",
                puntaje=15.0,
                peso=15.0,
                fecha="2026-09-12",
                tipo="tarea",
            ),
            2: Nota(
                id=2,
                curso_id=1,
                nombre="Parcial 1",
                puntaje=13.0,
                peso=25.0,
                fecha="2026-10-05",
                tipo="examen",
            ),
            3: Nota(
                id=3,
                curso_id=2,
                nombre="Quiz 1",
                puntaje=18.0,
                peso=10.0,
                fecha="2026-09-18",
                tipo="quiz",
            ),
            4: Nota(
                id=4,
                curso_id=4,
                nombre="Parcial 1",
                puntaje=13.0,
                peso=30.0,
                fecha="2026-10-10",
                tipo="examen",
            ),
        }
        self._siguiente_id = 5

    def listar(self) -> list[Nota]:
        return list(self._notas.values())

    def obtener(self, nota_id: int) -> Nota | None:
        return self._notas.get(nota_id)

    def listar_por_curso(self, curso_id: int) -> list[Nota]:
        return [n for n in self._notas.values() if n.curso_id == curso_id]

    def agregar(self, datos: NotaCreate) -> Nota:
        nota = Nota(id=self._siguiente_id, **datos.model_dump())
        self._notas[nota.id] = nota
        self._siguiente_id += 1
        return nota

    def actualizar(self, nota_id: int, datos: NotaUpdate) -> Nota | None:
        if nota_id not in self._notas:
            return None
        actualizada = Nota(id=nota_id, **datos.model_dump())
        self._notas[nota_id] = actualizada
        return actualizada

    def eliminar(self, nota_id: int) -> bool:
        return self._notas.pop(nota_id, None) is not None


nota_repository = NotaRepository()