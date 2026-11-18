from backend.database import get_db_cursor
from backend.schemas.evaluaciones import Evaluacion, EvaluacionCreate, EvaluacionUpdate


class EvaluacionRepository:
    def listar_por_curso(self, id_curso: int) -> list[Evaluacion]:
        query = """
            SELECT idEvaluacion, idCurso, idTipoEvaluacion, nombre,
                   ponderacion, notaMaxima, notaObtenida, fechaEvaluacion
            FROM Evaluacion WHERE idCurso = ? ORDER BY idEvaluacion;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_curso,))
            return [self._row(r) for r in cursor.fetchall()]

    def ponderacion_total(self, id_curso: int, excluir_id: int | None = None) -> float:
        if excluir_id is None:
            query = "SELECT COALESCE(SUM(ponderacion), 0) FROM Evaluacion WHERE idCurso = ?;"
            params = (id_curso,)
        else:
            query = "SELECT COALESCE(SUM(ponderacion), 0) FROM Evaluacion WHERE idCurso = ? AND idEvaluacion <> ?;"
            params = (id_curso, excluir_id)
        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
        return float(row[0] or 0) if row else 0.0

    def obtener(self, id_evaluacion: int) -> Evaluacion | None:
        query = """
            SELECT idEvaluacion, idCurso, idTipoEvaluacion, nombre,
                   ponderacion, notaMaxima, notaObtenida, fechaEvaluacion
            FROM Evaluacion WHERE idEvaluacion = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_evaluacion,))
            r = cursor.fetchone()
        return None if r is None else self._row(r)

    def agregar(self, datos: EvaluacionCreate) -> Evaluacion:
        # Recuperar todas las columnas mediante OUTPUT en la misma sentencia evita
        # abrir una segunda conexión mientras el INSERT todavía no está confirmado.
        # Consultar el registro desde otra conexión antes del commit podía dejar
        # bloqueada la petición esperando a que terminara la primera transacción.
        query = """
            INSERT INTO Evaluacion
                (idCurso, idTipoEvaluacion, nombre, ponderacion, notaMaxima, notaObtenida, fechaEvaluacion)
            OUTPUT
                INSERTED.idEvaluacion,
                INSERTED.idCurso,
                INSERTED.idTipoEvaluacion,
                INSERTED.nombre,
                INSERTED.ponderacion,
                INSERTED.notaMaxima,
                INSERTED.notaObtenida,
                INSERTED.fechaEvaluacion
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        with get_db_cursor() as cursor:
            cursor.execute(
                query,
                (
                    datos.id_curso,
                    datos.id_tipo_evaluacion,
                    datos.nombre,
                    datos.ponderacion,
                    20,
                    datos.nota_obtenida,
                    datos.fecha_evaluacion,
                ),
            )
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear evaluación.")
            return self._row(row)

    def actualizar(self, id_evaluacion: int, datos: EvaluacionUpdate) -> Evaluacion | None:
        query = """
            UPDATE Evaluacion
            SET idTipoEvaluacion = ?, nombre = ?, ponderacion = ?,
                notaMaxima = 20, notaObtenida = ?, fechaEvaluacion = ?
            WHERE idEvaluacion = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(
                query,
                (
                    datos.id_tipo_evaluacion,
                    datos.nombre,
                    datos.ponderacion,
                    datos.nota_obtenida,
                    datos.fecha_evaluacion,
                    id_evaluacion,
                ),
            )
            if cursor.rowcount == 0:
                return None
        return self.obtener(id_evaluacion)

    def eliminar(self, id_evaluacion: int) -> bool:
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM Evaluacion WHERE idEvaluacion = ?;", (id_evaluacion,))
            return cursor.rowcount > 0

    @staticmethod
    def _row(r: tuple) -> Evaluacion:
        return Evaluacion(
            id_evaluacion=int(r[0]),
            id_curso=int(r[1]),
            id_tipo_evaluacion=int(r[2]),
            nombre=str(r[3]),
            ponderacion=float(r[4]),
            nota_maxima=float(r[5]),
            nota_obtenida=float(r[6]) if r[6] is not None else None,
            fecha_evaluacion=r[7],
        )


evaluacion_repository = EvaluacionRepository()
