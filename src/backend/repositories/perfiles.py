from backend.database import get_db_cursor
from backend.schemas.perfil import Perfil, PerfilUpdate


class PerfilRepository:
    def create(
        self,
        id_usuario: int,
        nombres: str,
        apellidos: str,
        universidad: str | None = None,
        carrera: str | None = None,
        ciclo: str | None = None,
    ) -> Perfil:
        query = """
            INSERT INTO PerfilUsuario (idUsuario, nombres, apellidos, universidad, carrera, ciclo)
            OUTPUT INSERTED.idPerfil
            VALUES (?, ?, ?, ?, ?, ?);
        """
        with get_db_cursor() as cursor:
            cursor.execute(
                query, (id_usuario, nombres, apellidos, universidad, carrera, ciclo)
            )
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError("No se pudo crear perfil.")
            id_perfil = int(row[0])
        return Perfil(
            id_perfil=id_perfil,
            id_usuario=id_usuario,
            nombres=nombres,
            apellidos=apellidos,
            universidad=universidad,
            carrera=carrera,
            ciclo=ciclo,
        )

    def get_by_usuario(self, id_usuario: int) -> Perfil | None:
        query = """
            SELECT idPerfil, idUsuario, nombres, apellidos, universidad, carrera, ciclo, fotoUrl
            FROM PerfilUsuario WHERE idUsuario = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (id_usuario,))
            r = cursor.fetchone()
        if r is None:
            return None
        return Perfil(
            id_perfil=int(r[0]),
            id_usuario=int(r[1]),
            nombres=str(r[2]),
            apellidos=str(r[3]),
            universidad=r[4],
            carrera=r[5],
            ciclo=r[6],
            foto_url=r[7],
        )

    def update(self, id_usuario: int, datos: PerfilUpdate) -> Perfil | None:
        query = """
            UPDATE PerfilUsuario
            SET nombres = ?, apellidos = ?, universidad = ?, carrera = ?,
                ciclo = ?, fotoUrl = ?, fechaModificacion = SYSDATETIME()
            WHERE idUsuario = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(
                query,
                (
                    datos.nombres,
                    datos.apellidos,
                    datos.universidad,
                    datos.carrera,
                    datos.ciclo,
                    datos.foto_url,
                    id_usuario,
                ),
            )
            if cursor.rowcount == 0:
                return None
        return self.get_by_usuario(id_usuario)


perfil_repository = PerfilRepository()
