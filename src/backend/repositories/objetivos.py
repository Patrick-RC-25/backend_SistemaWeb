from backend.database import get_db_cursor
from backend.schemas.objetivos import Objetivo, ObjetivoCreate, ObjetivoUpdate


class ObjetivoRepository:
    def listar(self, id_usuario: int) -> list[Objetivo]:
        q = """
            SELECT idObjetivo, idUsuario, idCurso, titulo, descripcion,
                   fechaInicio, fechaLimite, progreso, estado
            FROM ObjetivoAcademico WHERE idUsuario = ?
            ORDER BY fechaLimite ASC;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_usuario,))
            return [self._row(r) for r in c.fetchall()]

    def obtener(self, id_objetivo: int) -> Objetivo | None:
        q = """
            SELECT idObjetivo, idUsuario, idCurso, titulo, descripcion,
                   fechaInicio, fechaLimite, progreso, estado
            FROM ObjetivoAcademico WHERE idObjetivo = ?;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_objetivo,))
            r = c.fetchone()
        return None if r is None else self._row(r)

    def agregar(self, id_usuario: int, d: ObjetivoCreate) -> Objetivo:
        q = """
            INSERT INTO ObjetivoAcademico
              (idUsuario, idCurso, titulo, descripcion, fechaInicio, fechaLimite, progreso, estado)
            OUTPUT INSERTED.idObjetivo
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pendiente');
        """
        with get_db_cursor() as c:
            c.execute(
                q,
                (
                    id_usuario,
                    d.id_curso,
                    d.titulo,
                    d.descripcion,
                    d.fecha_inicio,
                    d.fecha_limite,
                    d.progreso,
                ),
            )
            row = c.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear objetivo.")
            return self.obtener(int(row[0]))  # type: ignore[return-value]

    def actualizar(self, id_objetivo: int, d: ObjetivoUpdate) -> Objetivo | None:
        q = """
            UPDATE ObjetivoAcademico
            SET idCurso = ?, titulo = ?, descripcion = ?, fechaInicio = ?,
                fechaLimite = ?, progreso = ?, estado = ?
            WHERE idObjetivo = ?;
        """
        with get_db_cursor() as c:
            c.execute(
                q,
                (
                    d.id_curso,
                    d.titulo,
                    d.descripcion,
                    d.fecha_inicio,
                    d.fecha_limite,
                    d.progreso,
                    d.estado,
                    id_objetivo,
                ),
            )
            if c.rowcount == 0:
                return None
        return self.obtener(id_objetivo)

    def eliminar(self, id_objetivo: int) -> bool:
        with get_db_cursor() as c:
            c.execute("DELETE FROM ObjetivoAcademico WHERE idObjetivo = ?;", (id_objetivo,))
            return c.rowcount > 0

    @staticmethod
    def _row(r: tuple) -> Objetivo:
        return Objetivo(
            id_objetivo=int(r[0]),
            id_usuario=int(r[1]),
            id_curso=int(r[2]) if r[2] is not None else None,
            titulo=str(r[3]),
            descripcion=r[4],
            fecha_inicio=r[5],
            fecha_limite=r[6],
            progreso=float(r[7]),
            estado=str(r[8]),
        )


objetivo_repository = ObjetivoRepository()
