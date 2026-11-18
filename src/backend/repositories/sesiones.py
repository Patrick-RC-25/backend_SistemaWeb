from datetime import datetime

from backend.database import get_db_cursor
from backend.schemas.sesiones import Sesion, SesionCreate, SesionUpdate


class SesionRepository:
    def listar(self, id_usuario: int) -> list[Sesion]:
        q = """
            SELECT idSesion, idUsuario, idCurso, idTarea, titulo,
                   fechaInicioProgramada, fechaFinProgramada,
                   fechaInicioReal, fechaFinReal, estado, notas
            FROM SesionEstudio WHERE idUsuario = ?
            ORDER BY fechaInicioProgramada DESC;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_usuario,))
            return [self._row(r) for r in c.fetchall()]

    def listar_hoy(self, id_usuario: int) -> list[Sesion]:
        q = """
            SELECT idSesion, idUsuario, idCurso, idTarea, titulo,
                   fechaInicioProgramada, fechaFinProgramada,
                   fechaInicioReal, fechaFinReal, estado, notas
            FROM SesionEstudio
            WHERE idUsuario = ?
              AND CAST(fechaInicioProgramada AS DATE) = CAST(SYSDATETIME() AS DATE)
            ORDER BY fechaInicioProgramada;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_usuario,))
            return [self._row(r) for r in c.fetchall()]

    def obtener(self, id_sesion: int) -> Sesion | None:
        q = """
            SELECT idSesion, idUsuario, idCurso, idTarea, titulo,
                   fechaInicioProgramada, fechaFinProgramada,
                   fechaInicioReal, fechaFinReal, estado, notas
            FROM SesionEstudio WHERE idSesion = ?;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_sesion,))
            r = c.fetchone()
        return None if r is None else self._row(r)

    def agregar(self, id_usuario: int, d: SesionCreate) -> Sesion:
        q = """
            INSERT INTO SesionEstudio
              (idUsuario, idCurso, idTarea, titulo, fechaInicioProgramada, fechaFinProgramada, notas, estado)
            OUTPUT
                INSERTED.idSesion, INSERTED.idUsuario, INSERTED.idCurso,
                INSERTED.idTarea, INSERTED.titulo, INSERTED.fechaInicioProgramada,
                INSERTED.fechaFinProgramada, INSERTED.fechaInicioReal,
                INSERTED.fechaFinReal, INSERTED.estado, INSERTED.notas
            VALUES (?, ?, ?, ?, ?, ?, ?, 'programada');
        """
        with get_db_cursor() as c:
            c.execute(
                q,
                (
                    id_usuario,
                    d.id_curso,
                    d.id_tarea,
                    d.titulo,
                    d.fecha_inicio_programada,
                    d.fecha_fin_programada,
                    d.notas,
                ),
            )
            row = c.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear sesión.")
            return self._row(row)

    def actualizar(self, id_sesion: int, d: SesionUpdate) -> Sesion | None:
        q = """
            UPDATE SesionEstudio
            SET idCurso = ?, idTarea = ?, titulo = ?,
                fechaInicioProgramada = ?, fechaFinProgramada = ?,
                notas = ?, estado = ?
            WHERE idSesion = ?;
        """
        with get_db_cursor() as c:
            c.execute(
                q,
                (
                    d.id_curso,
                    d.id_tarea,
                    d.titulo,
                    d.fecha_inicio_programada,
                    d.fecha_fin_programada,
                    d.notas,
                    d.estado,
                    id_sesion,
                ),
            )
            if c.rowcount == 0:
                return None
        return self.obtener(id_sesion)

    def iniciar(self, id_sesion: int) -> Sesion | None:
        with get_db_cursor() as c:
            c.execute(
                """
                UPDATE SesionEstudio
                SET estado = 'en_progreso', fechaInicioReal = SYSDATETIME()
                WHERE idSesion = ? AND estado = 'programada';
                """,
                (id_sesion,),
            )
            if c.rowcount == 0:
                return None
        return self.obtener(id_sesion)

    def finalizar(self, id_sesion: int) -> Sesion | None:
        with get_db_cursor() as c:
            c.execute(
                """
                UPDATE SesionEstudio
                SET estado = 'completada', fechaFinReal = SYSDATETIME(),
                    fechaInicioReal = COALESCE(fechaInicioReal, SYSDATETIME())
                WHERE idSesion = ? AND estado IN ('programada', 'en_progreso');
                """,
                (id_sesion,),
            )
            if c.rowcount == 0:
                return None
        return self.obtener(id_sesion)

    def cancelar(self, id_sesion: int) -> Sesion | None:
        with get_db_cursor() as c:
            c.execute(
                "UPDATE SesionEstudio SET estado = 'cancelada' WHERE idSesion = ?;",
                (id_sesion,),
            )
            if c.rowcount == 0:
                return None
        return self.obtener(id_sesion)

    def eliminar(self, id_sesion: int) -> bool:
        with get_db_cursor() as c:
            c.execute("DELETE FROM SesionEstudio WHERE idSesion = ?;", (id_sesion,))
            return c.rowcount > 0

    @staticmethod
    def _row(r: tuple) -> Sesion:
        return Sesion(
            id_sesion=int(r[0]),
            id_usuario=int(r[1]),
            id_curso=int(r[2]) if r[2] is not None else None,
            id_tarea=int(r[3]) if r[3] is not None else None,
            titulo=str(r[4]),
            fecha_inicio_programada=r[5],
            fecha_fin_programada=r[6],
            fecha_inicio_real=r[7],
            fecha_fin_real=r[8],
            estado=str(r[9]),
            notas=r[10],
        )


sesion_repository = SesionRepository()
