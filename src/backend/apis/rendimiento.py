from typing import Annotated

from fastapi import APIRouter, Depends

from backend.apis.deps import get_current_user
from backend.repositories.cursos import curso_repository
from backend.schemas.auth import UsuarioResponse
from backend.schemas.rendimiento import CursoRendimiento, RendimientoResumen

router = APIRouter(prefix="/rendimiento", tags=["rendimiento"])
UserDep = Annotated[UsuarioResponse, Depends(get_current_user)]


@router.get("", response_model=RendimientoResumen)
def obtener_rendimiento(user: UserDep) -> RendimientoResumen:
    cursos = curso_repository.listar_por_usuario(user.id_usuario)
    items: list[CursoRendimiento] = []
    bajo: list[str] = []
    reco: list[str] = []
    promedios: list[float] = []

    for c in cursos:
        prom = c.promedio_actual
        obj = c.nota_objetivo
        dif = None
        if prom is not None and obj is not None:
            dif = round(prom - obj, 2)
            if prom < obj:
                bajo.append(c.nombre)
                reco.append(
                    f"Refuerza «{c.nombre}»: vas {abs(dif)} pts bajo tu objetivo ({obj})."
                )
        if prom is not None:
            promedios.append(prom)
        items.append(
            CursoRendimiento(
                id_curso=c.id_curso,
                nombre=c.nombre,
                promedio=prom,
                nota_objetivo=obj,
                diferencia=dif,
            )
        )

    general = round(sum(promedios) / len(promedios), 2) if promedios else None
    if general is not None and general >= 16:
        reco.append("Buen ritmo general. Mantén las sesiones de estudio planificadas.")
    elif general is not None:
        reco.append("Prioriza los cursos con menor promedio y revisa sus evaluaciones pendientes.")

    return RendimientoResumen(
        promedio_general=general,
        cursos=items,
        cursos_bajo_objetivo=bajo,
        recomendaciones=reco,
    )
