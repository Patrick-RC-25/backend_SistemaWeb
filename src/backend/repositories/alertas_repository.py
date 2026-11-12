from backend.schemas.alertas_schema import Alerta, AlertaCreate


class AlertaRepository:
    def __init__(self) -> None:
        self._alertas: dict[int, Alerta] = {
            1: Alerta(
                id=1,
                tipo="evaluacion",
                prioridad="urgente",
                titulo="Parcial de Sistemas Operativos",
                curso_nombre="Sistemas Operativos",
                fecha="Mañana · 8:00 a. m.",
                detalle="Tu promedio actual es 13.8. Necesitas 16.2 en este parcial.",
                atendida=False,
            ),
            2: Alerta(
                id=2,
                tipo="tarea",
                prioridad="importante",
                titulo="Entrega del proyecto SQL",
                curso_nombre="Bases de Datos",
                fecha="En 3 días · 11:59 p. m.",
                detalle="La entrega representa el 25% del curso.",
                atendida=False,
            ),
            3: Alerta(
                id=3,
                tipo="revision",
                prioridad="importante",
                titulo="Curso con tendencia descendente",
                curso_nombre="Matemáticas Superiores",
                fecha="Revisión recomendada esta semana",
                detalle="Tu nota bajó 0.8 puntos en dos evaluaciones.",
                atendida=False,
            ),
            4: Alerta(
                id=4,
                tipo="tarea",
                prioridad="sugerencia",
                titulo="Lectura de paper de redes",
                curso_nombre="Redes de Computadoras",
                fecha="Viernes · 23:59",
                detalle="Resumen de 2 páginas del paper asignado.",
                atendida=True,
            ),
        }
        self._siguiente_id = 5

    def listar(self) -> list[Alerta]:
        return list(self._alertas.values())

    def obtener(self, alerta_id: int) -> Alerta | None:
        return self._alertas.get(alerta_id)

    def agregar(self, datos: AlertaCreate) -> Alerta:
        alerta = Alerta(id=self._siguiente_id, **datos.model_dump())
        self._alertas[alerta.id] = alerta
        self._siguiente_id += 1
        return alerta

    def marcar_atendida(self, alerta_id: int) -> Alerta | None:
        alerta = self._alertas.get(alerta_id)
        if alerta is None:
            return None
        actualizada = alerta.model_copy(update={"atendida": True})
        self._alertas[alerta_id] = actualizada
        return actualizada

    def eliminar(self, alerta_id: int) -> bool:
        return self._alertas.pop(alerta_id, None) is not None


alerta_repository = AlertaRepository()