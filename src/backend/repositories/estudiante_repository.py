from backend.schemas.estudiante_schema import Estudiante, EstudianteUpdate


class EstudianteRepository:
    def __init__(self) -> None:
        self._estudiante = Estudiante(
            id=1,
            nombres="Carlos",
            apellidos="Mendoza Rojas",
            correo="carlos.mendoza@upeu.edu.pe",
            carrera="Ingeniería de Sistemas",
            semestre=6,
            iniciales="CM",
        )

    def obtener(self) -> Estudiante:
        return self._estudiante

    def actualizar(self, datos: EstudianteUpdate) -> Estudiante:
        self._estudiante = Estudiante(
            id=self._estudiante.id,
            iniciales=self._iniciales(datos.nombres, datos.apellidos),
            **datos.model_dump(),
        )
        return self._estudiante

    @staticmethod
    def _iniciales(nombres: str, apellidos: str) -> str:
        primera = nombres.strip()[:1]
        segunda = apellidos.strip()[:1]
        return f"{primera}{segunda}".upper()


estudiante_repository = EstudianteRepository()
