from backend.schemas.cursos_schema import Curso, CursoCreate, CursoUpdate


class CursoRepository:
    def __init__(self) -> None:
        self._cursos: dict[int, Curso] = {
            1: Curso(
                id=1,
                nombre="Matemáticas Superiores",
                codigo="MAT-301",
                creditos=4,
                promedio=14.2,
                promedio_anterior=15.0,
                docente="Ing. Rosa Quispe",
            ),
            2: Curso(
                id=2,
                nombre="Algoritmos y Estructuras",
                codigo="SIS-210",
                creditos=4,
                promedio=17.5,
                promedio_anterior=17.0,
                docente="Mg. Luis Huamán",
            ),
            3: Curso(
                id=3,
                nombre="Bases de Datos",
                codigo="SIS-220",
                creditos=3,
                promedio=16.1,
                promedio_anterior=15.8,
                docente="Ing. Ana Cerrón",
            ),
            4: Curso(
                id=4,
                nombre="Sistemas Operativos",
                codigo="SIS-230",
                creditos=4,
                promedio=13.8,
                promedio_anterior=14.5,
                docente="Dr. Pedro Vargas",
            ),
            5: Curso(
                id=5,
                nombre="Redes de Computadoras",
                codigo="SIS-240",
                creditos=3,
                promedio=15.9,
                promedio_anterior=15.5,
                docente="Ing. María Torres",
            ),
            6: Curso(
                id=6,
                nombre="Ingeniería de Software",
                codigo="SIS-250",
                creditos=4,
                promedio=16.4,
                promedio_anterior=16.0,
                docente="Mg. Javier Ríos",
            ),
        }
        self._siguiente_id = 7

    def listar(self) -> list[Curso]:
        return list(self._cursos.values())

    def obtener(self, curso_id: int) -> Curso | None:
        return self._cursos.get(curso_id)

    def existe(self, curso_id: int) -> bool:
        return curso_id in self._cursos

    def agregar(self, datos: CursoCreate) -> Curso:
        curso = Curso(
            id=self._siguiente_id,
            promedio_anterior=datos.promedio,
            **datos.model_dump(),
        )
        self._cursos[curso.id] = curso
        self._siguiente_id += 1
        return curso

    def actualizar(self, curso_id: int, datos: CursoUpdate) -> Curso | None:
        anterior = self._cursos.get(curso_id)
        if anterior is None:
            return None
        actualizado = Curso(
            id=curso_id,
            promedio_anterior=anterior.promedio,
            **datos.model_dump(),
        )
        self._cursos[curso_id] = actualizado
        return actualizado

    def eliminar(self, curso_id: int) -> bool:
        return self._cursos.pop(curso_id, None) is not None


curso_repository = CursoRepository()