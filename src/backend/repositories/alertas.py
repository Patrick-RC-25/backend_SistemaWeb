from backend.database import get_db_cursor
from backend.schemas.alertas import Alerta, AlertaCreate


class AlertaRepository:
    def listar_por_usuario(self, id_usuario: int) -> list[Alerta]:
        query = """
            SELECT idAlerta, idUsuario, idCurso, idTarea, idTipoAlerta,
                   titulo, mensaje, fechaProgramada, leida
            FROM Alerta
            WHERE idUsuario = ?
            ORDER BY fechaCreacion DESC;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_usuario,))
            return [self._row(r) for r in cursor.fetchall()]

    def obtener(self, id_alerta: int) -> Alerta | None:
        query = """
            SELECT idAlerta, idUsuario, idCurso, idTarea, idTipoAlerta,
                   titulo, mensaje, fechaProgramada, leida
            FROM Alerta WHERE idAlerta = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_alerta,))
            r = cursor.fetchone()
        return None if r is None else self._row(r)

    def agregar(self, id_usuario: int, datos: AlertaCreate) -> Alerta:
        query = """
            INSERT INTO Alerta (idUsuario, idCurso, idTarea, idTipoAlerta, titulo, mensaje, fechaProgramada)
            OUTPUT
                INSERTED.idAlerta, INSERTED.idUsuario, INSERTED.idCurso,
                INSERTED.idTarea, INSERTED.idTipoAlerta, INSERTED.titulo,
                INSERTED.mensaje, INSERTED.fechaProgramada, INSERTED.leida
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        with get_db_cursor() as cursor:
            cursor.execute(
                query,
                (
                    id_usuario,
                    datos.id_curso,
                    datos.id_tarea,
                    datos.id_tipo_alerta,
                    datos.titulo,
                    datos.mensaje,
                    datos.fecha_programada,
                ),
            )
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear alerta.")
            return self._row(row)

    def marcar_leida(self, id_alerta: int) -> Alerta | None:
        with get_db_cursor() as cursor:
            cursor.execute("UPDATE Alerta SET leida = 1 WHERE idAlerta = ?;", (id_alerta,))
            if cursor.rowcount == 0:
                return None
        return self.obtener(id_alerta)

    def eliminar(self, id_alerta: int) -> bool:
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM Alerta WHERE idAlerta = ?;", (id_alerta,))
            return cursor.rowcount > 0

    @staticmethod
    def _row(r: tuple) -> Alerta:
        return Alerta(
            id_alerta=int(r[0]),
            id_usuario=int(r[1]),
            id_curso=int(r[2]) if r[2] is not None else None,
            id_tarea=int(r[3]) if r[3] is not None else None,
            id_tipo_alerta=int(r[4]),
            titulo=str(r[5]),
            mensaje=str(r[6]),
            fecha_programada=r[7],
            leida=bool(r[8]),
        )


alerta_repository = AlertaRepository()
