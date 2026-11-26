from backend.database import get_db_cursor
from backend.schemas.objetivos import Objetivo, ObjetivoCreate, ObjetivoUpdate


class ObjetivoRepository:
    _SELECT = """
        SELECT o.idObjetivo, o.idUsuario, o.idCurso, o.titulo, o.descripcion,
               o.fechaInicio, o.fechaLimite,
               CASE WHEN COUNT(t.idTarea) = 0 THEN 0
                    ELSE CAST(100.0 * SUM(CASE WHEN t.estado = 'completada' THEN 1 ELSE 0 END)
                              / COUNT(t.idTarea) AS DECIMAL(5,2)) END AS progreso_calculado,
               CASE WHEN o.estado = 'cancelado' THEN 'cancelado'
                    WHEN COUNT(t.idTarea) > 0 AND
                         SUM(CASE WHEN t.estado = 'completada' THEN 1 ELSE 0 END) = COUNT(t.idTarea)
                         THEN 'completado'
                    WHEN SUM(CASE WHEN t.estado = 'completada' THEN 1 ELSE 0 END) > 0
                         THEN 'en_progreso'
                    ELSE 'pendiente' END AS estado_calculado,
               COUNT(t.idTarea) AS total_tareas,
               COALESCE(SUM(CASE WHEN t.estado = 'completada' THEN 1 ELSE 0 END), 0) AS tareas_completadas
        FROM ObjetivoAcademico o
        LEFT JOIN Tarea t ON t.idObjetivo = o.idObjetivo AND t.estado <> 'cancelada'
    """
    _GROUP = """
        GROUP BY o.idObjetivo, o.idUsuario, o.idCurso, o.titulo, o.descripcion,
                 o.fechaInicio, o.fechaLimite, o.estado
    """

    def listar(self, id_usuario: int) -> list[Objetivo]:
        q = self._SELECT + " WHERE o.idUsuario = ? " + self._GROUP + """
            ORDER BY CASE WHEN o.fechaLimite IS NULL THEN 1 ELSE 0 END, o.fechaLimite ASC;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_usuario,))
            return [self._row(row) for row in c.fetchall()]

    def obtener(self, id_objetivo: int) -> Objetivo | None:
        q = self._SELECT + " WHERE o.idObjetivo = ? " + self._GROUP + ";"
        with get_db_cursor() as c:
            c.execute(q, (id_objetivo,))
            row = c.fetchone()
        return None if row is None else self._row(row)

    def agregar(self, id_usuario: int, d: ObjetivoCreate) -> Objetivo:
        q = """
            INSERT INTO ObjetivoAcademico
                (idUsuario, idCurso, titulo, descripcion, fechaInicio, fechaLimite)
            OUTPUT INSERTED.idObjetivo
            VALUES (?, ?, ?, ?, ?, ?);
        """
        with get_db_cursor() as c:
            c.execute(q, (id_usuario, d.id_curso, d.titulo, d.descripcion,
                          d.fecha_inicio, d.fecha_limite))
            row = c.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear objetivo.")
            id_objetivo = int(row[0])
        result = self.obtener(id_objetivo)
        if result is None:
            raise RuntimeError("No se pudo recuperar el objetivo creado.")
        return result

    def actualizar(self, id_objetivo: int, d: ObjetivoUpdate) -> Objetivo | None:
        q = """
            UPDATE ObjetivoAcademico
            SET idCurso = ?, titulo = ?, descripcion = ?, fechaInicio = ?, fechaLimite = ?
            WHERE idObjetivo = ?;
        """
        with get_db_cursor() as c:
            c.execute(q, (d.id_curso, d.titulo, d.descripcion, d.fecha_inicio,
                          d.fecha_limite, id_objetivo))
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
            id_objetivo=int(r[0]), id_usuario=int(r[1]),
            id_curso=int(r[2]) if r[2] is not None else None,
            titulo=str(r[3]), descripcion=r[4], fecha_inicio=r[5], fecha_limite=r[6],
            progreso=float(r[7] or 0), estado=str(r[8]),
            total_tareas=int(r[9] or 0), tareas_completadas=int(r[10] or 0),
        )


objetivo_repository = ObjetivoRepository()
