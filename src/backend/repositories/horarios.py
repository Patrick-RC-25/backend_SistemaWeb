from backend.database import get_db_cursor
from backend.schemas.horarios import Horario, HorarioCreate, HorarioUpdate


class HorarioRepository:
    def listar_por_curso(self, id_curso: int) -> list[Horario]:
        q = """
            SELECT idHorario, idCurso, diaSemana, horaInicio, horaFin, aula
            FROM HorarioCurso WHERE idCurso = ?
            ORDER BY diaSemana, horaInicio;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_curso,))
            return [self._row(r) for r in c.fetchall()]

    def listar_por_usuario(self, id_usuario: int) -> list[Horario]:
        q = """
            SELECT h.idHorario, h.idCurso, h.diaSemana, h.horaInicio, h.horaFin, h.aula
            FROM HorarioCurso h
            INNER JOIN Curso c ON c.idCurso = h.idCurso
            INNER JOIN PeriodoAcademico p ON p.idPeriodo = c.idPeriodo
            WHERE p.idUsuario = ? AND p.estado = 'activo' AND c.estado = 1
            ORDER BY h.diaSemana, h.horaInicio;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_usuario,))
            return [self._row(r) for r in c.fetchall()]

    def obtener(self, id_horario: int) -> Horario | None:
        q = """
            SELECT idHorario, idCurso, diaSemana, horaInicio, horaFin, aula
            FROM HorarioCurso WHERE idHorario = ?;
        """
        with get_db_cursor() as c:
            c.execute(q, (id_horario,))
            r = c.fetchone()
        return None if r is None else self._row(r)

    def agregar(self, d: HorarioCreate) -> Horario:
        q = """
            INSERT INTO HorarioCurso (idCurso, diaSemana, horaInicio, horaFin, aula)
            OUTPUT INSERTED.idHorario
            VALUES (?, ?, ?, ?, ?);
        """
        with get_db_cursor() as c:
            c.execute(
                q,
                (d.id_curso, d.dia_semana, d.hora_inicio, d.hora_fin, d.aula),
            )
            row = c.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear horario.")
            return self.obtener(int(row[0]))  # type: ignore[return-value]

    def actualizar(self, id_horario: int, d: HorarioUpdate) -> Horario | None:
        q = """
            UPDATE HorarioCurso
            SET diaSemana = ?, horaInicio = ?, horaFin = ?, aula = ?
            WHERE idHorario = ?;
        """
        with get_db_cursor() as c:
            c.execute(
                q,
                (d.dia_semana, d.hora_inicio, d.hora_fin, d.aula, id_horario),
            )
            if c.rowcount == 0:
                return None
        return self.obtener(id_horario)

    def eliminar(self, id_horario: int) -> bool:
        with get_db_cursor() as c:
            c.execute("DELETE FROM HorarioCurso WHERE idHorario = ?;", (id_horario,))
            return c.rowcount > 0

    @staticmethod
    def _row(r: tuple) -> Horario:
        return Horario(
            id_horario=int(r[0]),
            id_curso=int(r[1]),
            dia_semana=int(r[2]),
            hora_inicio=r[3],
            hora_fin=r[4],
            aula=r[5],
        )


horario_repository = HorarioRepository()
