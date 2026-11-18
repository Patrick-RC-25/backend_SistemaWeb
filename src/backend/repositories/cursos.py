from backend.database import get_db_cursor
from backend.schemas.cursos import Curso, CursoCreate, CursoUpdate


class CursoRepository:
    def listar_por_usuario(self, id_usuario: int) -> list[Curso]:
        """Cursos de los periodos del usuario + promedio de vista si existe."""
        query = """
            SELECT c.idCurso, c.idPeriodo, c.nombre, c.codigo, c.docente,
                   c.creditos, c.color, c.notaObjetivo, c.estado,
                   v.promedioActual
            FROM Curso c
            INNER JOIN PeriodoAcademico p ON p.idPeriodo = c.idPeriodo
            LEFT JOIN vw_PromedioCurso v ON v.idCurso = c.idCurso
            WHERE p.idUsuario = ? AND p.estado = 'activo' AND c.estado = 1
            ORDER BY c.idCurso;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_usuario,))
            rows = cursor.fetchall()
        return [self._row(r) for r in rows]

    def obtener(self, id_curso: int) -> Curso | None:
        query = """
            SELECT c.idCurso, c.idPeriodo, c.nombre, c.codigo, c.docente,
                   c.creditos, c.color, c.notaObjetivo, c.estado,
                   v.promedioActual
            FROM Curso c
            LEFT JOIN vw_PromedioCurso v ON v.idCurso = c.idCurso
            WHERE c.idCurso = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_curso,))
            r = cursor.fetchone()
        return None if r is None else self._row(r)

    def pertenece_a_usuario(self, id_curso: int, id_usuario: int) -> bool:
        query = """
            SELECT 1
            FROM Curso c
            INNER JOIN PeriodoAcademico p ON p.idPeriodo = c.idPeriodo
            WHERE c.idCurso = ? AND p.idUsuario = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_curso, id_usuario))
            return cursor.fetchone() is not None

    def agregar(self, datos: CursoCreate) -> Curso:
        query = """
            INSERT INTO Curso (idPeriodo, nombre, codigo, docente, creditos, color, notaObjetivo)
            OUTPUT INSERTED.idCurso
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        with get_db_cursor() as cursor:
            cursor.execute(
                query,
                (
                    datos.id_periodo,
                    datos.nombre,
                    datos.codigo,
                    datos.docente,
                    datos.creditos,
                    datos.color,
                    datos.nota_objetivo,
                ),
            )
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear curso.")
            id_curso = int(row[0])
        return self.obtener(id_curso)  # type: ignore[return-value]

    def actualizar(self, id_curso: int, datos: CursoUpdate) -> Curso | None:
        query = """
            UPDATE Curso
            SET nombre = ?, codigo = ?, docente = ?, creditos = ?,
                color = ?, notaObjetivo = ?, estado = ?
            WHERE idCurso = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(
                query,
                (
                    datos.nombre,
                    datos.codigo,
                    datos.docente,
                    datos.creditos,
                    datos.color,
                    datos.nota_objetivo,
                    1 if datos.estado else 0,
                    id_curso,
                ),
            )
            if cursor.rowcount == 0:
                return None
        return self.obtener(id_curso)

    def eliminar(self, id_curso: int) -> bool:
        # Soft delete
        with get_db_cursor() as cursor:
            cursor.execute("UPDATE Curso SET estado = 0 WHERE idCurso = ?;", (id_curso,))
            return cursor.rowcount > 0

    @staticmethod
    def _row(r: tuple) -> Curso:
        return Curso(
            id_curso=int(r[0]),
            id_periodo=int(r[1]),
            nombre=str(r[2]),
            codigo=r[3],
            docente=r[4],
            creditos=int(r[5]) if r[5] is not None else None,
            color=r[6],
            nota_objetivo=float(r[7]) if r[7] is not None else None,
            estado=bool(r[8]),
            promedio_actual=float(r[9]) if r[9] is not None else None,
        )


curso_repository = CursoRepository()
