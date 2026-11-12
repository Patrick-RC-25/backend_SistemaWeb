from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.apis.alertas_api import router as alertas_router
from backend.apis.cursos_api import router as cursos_router
from backend.apis.notas_api import router as notas_router
from backend.services.exceptions import (
    AlertaNotFoundError,
    CursoInvalidoError,
    CursoNotFoundError,
    NotaNotFoundError,
)

app = FastAPI(
    title="CarlitoApp API",
    version="0.1.0",
    description="CRUD académico con almacenamiento en memoria (cursos, notas, alertas).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:4000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cursos_router)
app.include_router(notas_router)
app.include_router(alertas_router)


@app.get("/", tags=["salud"])
def mensaje() -> dict[str, str]:
    return {"mensaje": "Funciona"}


@app.exception_handler(CursoNotFoundError)
async def curso_not_found_handler(
    request: Request, exc: CursoNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(NotaNotFoundError)
async def nota_not_found_handler(
    request: Request, exc: NotaNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(AlertaNotFoundError)
async def alerta_not_found_handler(
    request: Request, exc: AlertaNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(CursoInvalidoError)
async def curso_invalido_handler(
    request: Request, exc: CursoInvalidoError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )
