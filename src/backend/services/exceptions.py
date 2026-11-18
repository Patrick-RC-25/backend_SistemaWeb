class UsuarioAlreadyExistsError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"El correo electrónico '{email}' ya se encuentra registrado.")


class InvalidCredentialsError(Exception):
    def __init__(self, message: str = "Email o contraseña incorrectos.") -> None:
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ForbiddenError(Exception):
    def __init__(self, message: str = "No autorizado.") -> None:
        super().__init__(message)


class BusinessRuleError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
