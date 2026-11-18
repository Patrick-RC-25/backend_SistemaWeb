from backend.repositories.estudiante_repository import (
    EstudianteRepository,
    estudiante_repository,
)
from backend.schemas.auth_schema import LoginRequest, LoginResponse
from backend.services.exceptions import CredencialesInvalidasError

DEMO_EMAIL = "demo@carlito.app"
DEMO_PASSWORD = "demo"


class AuthService:
    def __init__(self, repository: EstudianteRepository | None = None) -> None:
        self._repository = repository or estudiante_repository

    def login(self, datos: LoginRequest) -> LoginResponse:
        email = datos.email.strip().lower()
        if email != DEMO_EMAIL or datos.password != DEMO_PASSWORD:
            raise CredencialesInvalidasError()
        return LoginResponse(
            autenticado=True,
            estudiante=self._repository.obtener(),
        )


auth_service = AuthService()
