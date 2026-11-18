from datetime import date

from backend.database import get_db_cursor
from backend.schemas.periodos import Periodo, PeriodoCreate


class PeriodoRepository:
    def listar_por_usuario(self, id_usuario: int) -> list[Periodo]:
        query = """
            SELECT idPeriodo, idUsuario, nombre, fechaInicio, fechaFin, estado
            FROM PeriodoAcademico
            WHERE idUsuario = ?
            ORDER BY fechaInicio DESC;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_usuario,))
            rows = cursor.fetchall()
        return [self._row(r) for r in rows]

    def obtener(self, id_periodo: int) -> Periodo | None:
        query = """
            SELECT idPeriodo, idUsuario, nombre, fechaInicio, fechaFin, estado
            FROM PeriodoAcademico WHERE idPeriodo = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_periodo,))
            r = cursor.fetchone()
        return None if r is None else self._row(r)

    def create(self, id_usuario: int, datos: PeriodoCreate) -> Periodo:
        query = """
            INSERT INTO PeriodoAcademico (idUsuario, nombre, fechaInicio, fechaFin, estado)
            OUTPUT INSERTED.idPeriodo
            VALUES (?, ?, ?, ?, ?);
        """
        with get_db_cursor() as cursor:
            if datos.estado == "activo":
                cursor.execute(
                    "UPDATE PeriodoAcademico SET estado = 'finalizado' WHERE idUsuario = ? AND estado = 'activo';",
                    (id_usuario,),
                )
            cursor.execute(
                query,
                (id_usuario, datos.nombre, datos.fecha_inicio, datos.fecha_fin, datos.estado),
            )
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear periodo.")
            id_periodo = int(row[0])
        return Periodo(
            id_periodo=id_periodo,
            id_usuario=id_usuario,
            nombre=datos.nombre,
            fecha_inicio=datos.fecha_inicio,
            fecha_fin=datos.fecha_fin,
            estado=datos.estado,
        )

    def create_default(self, id_usuario: int) -> Periodo:
        hoy = date.today()
        fin = date(hoy.year if hoy.month < 8 else hoy.year + 1, 7 if hoy.month < 8 else 12, 31)
        datos = PeriodoCreate(
            nombre=f"Ciclo {hoy.year}",
            fecha_inicio=hoy,
            fecha_fin=fin,
            estado="activo",
        )
        return self.create(id_usuario, datos)

    @staticmethod
    def _row(r: tuple) -> Periodo:
        return Periodo(
            id_periodo=int(r[0]),
            id_usuario=int(r[1]),
            nombre=str(r[2]),
            fecha_inicio=r[3],
            fecha_fin=r[4],
            estado=str(r[5]),
        )


periodo_repository = PeriodoRepository()
