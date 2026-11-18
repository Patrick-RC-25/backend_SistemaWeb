from backend.database import get_db_cursor
from backend.schemas.tareas import Tarea, TareaCreate, TareaUpdate


class TareaRepository:
    def listar(self, id_usuario: int) -> list[Tarea]:
        q = """
            SELECT idTarea, idUsuario, idCurso, titulo, descripcion,
                   fechaVencimiento, prioridad, estado, fechaCompletada
            FROM Tarea WHERE idUsuario = ?
            ORDER BY
              CASE WHEN fechaVencimiento IS NULL THEN 1 ELSE 0 END,
              fechaVencimiento ASC;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_usuario,))
            return [self._row(r) for r in c.fetchall()]

    def obtener(self, id_tarea: int) -> Tarea | None:
        q = """
            SELECT idTarea, idUsuario, idCurso, titulo, descripcion,
                   fechaVencimiento, prioridad, estado, fechaCompletada
            FROM Tarea WHERE idTarea = ?;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_tarea,))
            r = c.fetchone()
        return None if r is None else self._row(r)

    def agregar(self, id_usuario: int, d: TareaCreate) -> Tarea:
        q = """
            INSERT INTO Tarea (idUsuario, idCurso, titulo, descripcion, fechaVencimiento, prioridad, estado)
            OUTPUT
                INSERTED.idTarea, INSERTED.idUsuario, INSERTED.idCurso,
                INSERTED.titulo, INSERTED.descripcion, INSERTED.fechaVencimiento,
                INSERTED.prioridad, INSERTED.estado, INSERTED.fechaCompletada
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        with get_db_cursor() as c:
            c.execute(
                q,
                (
                    id_usuario,
                    d.id_curso,
                    d.titulo,
                    d.descripcion,
                    d.fecha_vencimiento,
                    d.prioridad,
                    d.estado,
                ),
            )
            row = c.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear tarea.")
            return self._row(row)

    def actualizar(self, id_tarea: int, d: TareaUpdate) -> Tarea | None:
        fecha_comp = None
        if d.estado == "completada":
            fecha_comp_sql = "SYSDATETIME()"
        else:
            fecha_comp_sql = "NULL"
        q = f"""
            UPDATE Tarea
            SET idCurso = ?, titulo = ?, descripcion = ?, fechaVencimiento = ?,
                prioridad = ?, estado = ?,
                fechaCompletada = CASE WHEN ? = 'completada' THEN SYSDATETIME() ELSE NULL END
            WHERE idTarea = ?;
        """
        with get_db_cursor() as c:
            c.execute(
                q,
                (
                    d.id_curso,
                    d.titulo,
                    d.descripcion,
                    d.fecha_vencimiento,
                    d.prioridad,
                    d.estado,
                    d.estado,
                    id_tarea,
                ),
            )
            if c.rowcount == 0:
                return None
        return self.obtener(id_tarea)

    def eliminar(self, id_tarea: int) -> bool:
        with get_db_cursor() as c:
            c.execute("DELETE FROM Tarea WHERE idTarea = ?;", (id_tarea,))
            return c.rowcount > 0

    @staticmethod
    def _row(r: tuple) -> Tarea:
        return Tarea(
            id_tarea=int(r[0]),
            id_usuario=int(r[1]),
            id_curso=int(r[2]) if r[2] is not None else None,
            titulo=str(r[3]),
            descripcion=r[4],
            fecha_vencimiento=r[5],
            prioridad=str(r[6]),
            estado=str(r[7]),
            fecha_completada=r[8],
        )


tarea_repository = TareaRepository()
