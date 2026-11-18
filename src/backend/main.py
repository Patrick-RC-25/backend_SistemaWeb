from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pyodbc

from backend.apis.alertas import router as alertas_router
from backend.apis.auth import router as auth_router
from backend.apis.cursos import router as cursos_router
from backend.apis.dashboard import router as dashboard_router
from backend.apis.rendimiento import router as rendimiento_router
from backend.apis.evaluaciones import router as evaluaciones_router
from backend.apis.horarios import router as horarios_router
from backend.apis.objetivos import router as objetivos_router
from backend.apis.perfiles import router as perfiles_router
from backend.apis.periodos import router as periodos_router
from backend.apis.sesiones import router as sesiones_router
from backend.apis.tareas import router as tareas_router
from backend.database import test_connection
from backend.services.exceptions import (
    BusinessRuleError,
    ForbiddenError,
    InvalidCredentialsError,
    NotFoundError,
    UsuarioAlreadyExistsError,
)

app = FastAPI(
    title="RandomStudy API",
    version="0.3.0",
    description="RandomStudy: SQL Server (RandomStudyDB) + Argon2id + JWT, sin ORM.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router)
app.include_router(periodos_router)
app.include_router(cursos_router)
app.include_router(evaluaciones_router)
app.include_router(horarios_router)
app.include_router(tareas_router)
app.include_router(sesiones_router)
app.include_router(objetivos_router)
app.include_router(alertas_router)
app.include_router(perfiles_router)
app.include_router(dashboard_router)
app.include_router(rendimiento_router)


@app.get("/health", tags=["health"], response_model=None)
def health() -> JSONResponse:
    try:
        test_connection()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "ok", "database": "connected"},
        )
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "detail": str(exc)},
        )


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(BusinessRuleError)
async def business_rule_handler(request: Request, exc: BusinessRuleError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(ForbiddenError)
async def forbidden_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
    return JSONResponse(status_code=403, content={"detail": str(exc)})


@app.exception_handler(UsuarioAlreadyExistsError)
async def user_exists_handler(
    request: Request, exc: UsuarioAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(InvalidCredentialsError)
async def invalid_cred_handler(
    request: Request, exc: InvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(pyodbc.Error)
async def db_error_handler(request: Request, exc: pyodbc.Error) -> JSONResponse:
    # Detalle acotado para diagnosticar ODBC/.env sin filtrar secretos
    return JSONResponse(
        status_code=500,
        content={
            "detail": (
                "Error de base de datos. Verifica: SQL Server en marcha, "
                "base RandomStudyDB creada, ODBC Driver 17/18 y el archivo .env. "
                f"Detalle técnico: {exc}"
            )
        },
    )
