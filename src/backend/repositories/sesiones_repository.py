from backend.schemas.sesiones_schema import Sesion, SesionCreate


class SesionRepository:
    def __init__(self) -> None:
        self._sesiones: dict[int, Sesion] = {
            1: Sesion(
                id=1,
                curso_id=4,
                curso_nombre="Sistemas Operativos",
                titulo="Repaso de procesos y threads",
                descripcion=(
                    "Repasar capítulos 3 y 4 del Silberschatz. "
                    "Hacer ejercicios de sincronización."
                ),
                fecha="2026-11-12",
                hora_inicio="07:00",
                duracion_minutos=90,
                estado="pendiente",
            ),
            2: Sesion(
                id=2,
                curso_id=1,
                curso_nombre="Matemáticas Superiores",
                titulo="Series y transformadas",
                descripcion="Practicar problemas de series de Fourier y Laplace.",
                fecha="2026-11-12",
                hora_inicio="16:00",
                duracion_minutos=60,
                estado="pendiente",
            ),
            3: Sesion(
                id=3,
                curso_id=3,
                curso_nombre="Bases de Datos",
                titulo="Revisión del modelo ER del proyecto",
                descripcion="Validar normalización y relaciones antes de la entrega.",
                fecha="2026-11-13",
                hora_inicio="19:00",
                duracion_minutos=45,
                estado="pendiente",
            ),
            4: Sesion(
                id=4,
                curso_id=2,
                curso_nombre="Algoritmos y Estructuras",
                titulo="Árboles AVL y heaps",
                descripcion="Implementar inserción y balanceo en pseudocódigo.",
                fecha="2026-11-10",
                hora_inicio="10:00",
                duracion_minutos=75,
                estado="completada",
            ),
        }
        self._siguiente_id = 5

    def listar(self) -> list[Sesion]:
        return list(self._sesiones.values())

    def obtener(self, sesion_id: int) -> Sesion | None:
        return self._sesiones.get(sesion_id)

    def agregar(self, datos: SesionCreate, curso_nombre: str) -> Sesion:
        sesion = Sesion(
            id=self._siguiente_id,
            curso_nombre=curso_nombre,
            estado="pendiente",
            **datos.model_dump(),
        )
        self._sesiones[sesion.id] = sesion
        self._siguiente_id += 1
        return sesion

    def actualizar_estado(self, sesion_id: int, estado: str) -> Sesion | None:
        sesion = self._sesiones.get(sesion_id)
        if sesion is None:
            return None
        actualizada = sesion.model_copy(update={"estado": estado})
        self._sesiones[sesion_id] = actualizada
        return actualizada


sesion_repository = SesionRepository()
