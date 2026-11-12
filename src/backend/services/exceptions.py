class CursoNotFoundError(Exception):
    def __init__(self, curso_id: int) -> None:
        self.curso_id = curso_id
        super().__init__(f"No existe un curso con id {curso_id}.")


class NotaNotFoundError(Exception):
    def __init__(self, nota_id: int) -> None:
        self.nota_id = nota_id
        super().__init__(f"No existe una nota con id {nota_id}.")


class AlertaNotFoundError(Exception):
    def __init__(self, alerta_id: int) -> None:
        self.alerta_id = alerta_id
        super().__init__(f"No existe una alerta con id {alerta_id}.")


class CursoInvalidoError(Exception):
    def __init__(self, curso_id: int) -> None:
        self.curso_id = curso_id
        super().__init__(f"El curso con id {curso_id} no existe.")