"""Acceso a dbo.Usuario — SQL parametrizado."""

from datetime import date

from backend.database import get_db_cursor
from backend.schemas.periodos import PeriodoCreate


class UsuarioRepository:
    def exists_email(self, email: str) -> bool:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT 1 FROM Usuario WHERE email = ?;", (email,))
            return cursor.fetchone() is not None

    def get_by_email(self, email: str) -> tuple[int, str, str] | None:
        query = """
            SELECT idUsuario, email, contrasena
            FROM Usuario
            WHERE email = ? AND estado = 1;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (email,))
            row = cursor.fetchone()
        if row is None:
            return None
        return (int(row[0]), str(row[1]), str(row[2]))

    def get_by_id(self, id_usuario: int) -> tuple[int, str, str] | None:
        query = """
            SELECT idUsuario, email, contrasena
            FROM Usuario
            WHERE idUsuario = ? AND estado = 1;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_usuario,))
            row = cursor.fetchone()
        if row is None:
            return None
        return (int(row[0]), str(row[1]), str(row[2]))

    def create(self, email: str, contrasena_hash: str) -> tuple[int, str]:
        query = """
            INSERT INTO Usuario (email, contrasena)
            OUTPUT INSERTED.idUsuario
            VALUES (?, ?);
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (email, contrasena_hash))
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("No se pudo obtener idUsuario.")
            return (int(row[0]), email)

    def create_with_perfil_y_periodo(
        self,
        email: str,
        contrasena_hash: str,
        nombres: str,
        apellidos: str,
        universidad: str | None,
        carrera: str | None,
        ciclo: str | None,
    ) -> tuple[int, str]:
        """Crea Usuario + PerfilUsuario + PeriodoAcademico en la misma transacción."""
        hoy = date.today()
        fin = date(hoy.year if hoy.month < 8 else hoy.year + 1, 7 if hoy.month < 8 else 12, 31)
        nombre_periodo = f"Ciclo {hoy.year}"

        with get_db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Usuario (email, contrasena)
                OUTPUT INSERTED.idUsuario
                VALUES (?, ?);
                """,
                (email, contrasena_hash),
            )
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear el usuario.")
            id_usuario = int(row[0])

            cursor.execute(
                """
                INSERT INTO PerfilUsuario (idUsuario, nombres, apellidos, universidad, carrera, ciclo)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (id_usuario, nombres, apellidos, universidad, carrera, ciclo),
            )

            cursor.execute(
                """
                INSERT INTO PeriodoAcademico (idUsuario, nombre, fechaInicio, fechaFin, estado)
                VALUES (?, ?, ?, ?, 'activo');
                """,
                (id_usuario, nombre_periodo, hoy, fin),
            )

            return (id_usuario, email)

    def touch_ultimo_login(self, id_usuario: int) -> None:
        with get_db_cursor() as cursor:
            cursor.execute(
                "UPDATE Usuario SET fechaUltimoLogin = SYSDATETIME() WHERE idUsuario = ?;",
                (id_usuario,),
            )


usuario_repository = UsuarioRepository()
