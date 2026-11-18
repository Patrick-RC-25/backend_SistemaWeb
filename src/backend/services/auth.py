from backend.core.security import create_access_token, hash_password, verify_password
from backend.repositories.usuarios import UsuarioRepository, usuario_repository
from backend.schemas.auth import TokenResponse, UsuarioLogin, UsuarioRegistro
from backend.services.exceptions import InvalidCredentialsError, UsuarioAlreadyExistsError


class AuthService:
    def __init__(self, repository: UsuarioRepository | None = None) -> None:
        self._repository = repository or usuario_repository

    def registrar(self, datos: UsuarioRegistro) -> TokenResponse:
        email = datos.email
        if self._repository.exists_email(email):
            raise UsuarioAlreadyExistsError(email)

        contrasena_hash = hash_password(datos.contrasena)
        id_usuario, _ = self._repository.create_with_perfil_y_periodo(
            email=email,
            contrasena_hash=contrasena_hash,
            nombres=datos.nombres,
            apellidos=datos.apellidos,
            universidad=datos.universidad,
            carrera=datos.carrera,
            ciclo=datos.ciclo,
        )

        access_token = create_access_token(
            data={"sub": email, "id_usuario": id_usuario}
        )
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            email=email,
            id_usuario=id_usuario,
        )

    def login(self, datos: UsuarioLogin) -> TokenResponse:
        user = self._repository.get_by_email(datos.email)
        if user is None:
            raise InvalidCredentialsError()
        id_usuario, user_email, contrasena_hash = user
        if not verify_password(datos.contrasena, contrasena_hash):
            raise InvalidCredentialsError()

        self._repository.touch_ultimo_login(id_usuario)
        access_token = create_access_token(
            data={"sub": user_email, "id_usuario": id_usuario}
        )
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            email=user_email,
            id_usuario=id_usuario,
        )


auth_service = AuthService()
