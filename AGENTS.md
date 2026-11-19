# AGENTS.md

Backend de RandomStudy: FastAPI + SQL Server vía `pyodbc`, sin ORM. Layout `src/`, se importa como `backend.*` (nunca `src.backend.*`).

## Comandos

Desde la raíz de este repo (`backend_SistemaWeb-main`):

```powershell
Copy-Item .env.example .env   # completar SQL Server y JWT_SECRET_KEY
uv sync
uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

- Prerrequisitos: `uv`, Python >=3.12 (`.python-version` = 3.13), SQL Server con `../sql/RandomStudyDB.sql` ejecutado y ODBC Driver 18 (o 17 definiendo `DB_DRIVER`).
- No hay tests, linter, formatter ni typecheck configurados: no inventes `pytest`/`ruff`. Verifica con `uv run python -c "import backend.main"` y, con SQL Server arriba, `GET /health` (503 si falla la DB) y `/docs`.

## Arquitectura

- Flujo: `apis/*.py` (router + `Depends`) → `services/*.py` (reglas de negocio y propiedad) → `repositories/*.py` (SQL parametrizado con `?` y mapeo manual de filas) → `schemas/*.py` (Pydantic).
- Los routers se registran a mano en `src/backend/main.py`; un router nuevo no existe hasta agregarlo allí.
- Singletons a nivel de módulo (`tarea_service`, `curso_repository`) inyectados con `Depends(lambda: ...)`.
- Los servicios lanzan las excepciones de `services/exceptions.py`; `main.py` las traduce (404, 422, 403, 409, 401). No uses `HTTPException` en servicios. `pyodbc.Error` → 500.
- `get_db_cursor()` hace commit al salir y rollback ante excepción. En creates usa `OUTPUT INSERTED...` en el mismo cursor; no consultes el registro desde otra conexión antes del commit.
- Solo SQL Server/T-SQL: `SYSDATETIME()`, `CAST(... AS DATE)`, placeholders `?`. No agregues ORM ni SQL de otro motor.

## Convenciones no obvias

- Español en la API: Pydantic en snake_case (`id_curso`, `fecha_vencimiento`), columnas SQL en camelCase (`idCurso`, `fechaVencimiento`); el mapeo es manual en cada repositorio.
- Todo recurso de usuario se filtra por el `id_usuario` del JWT (`get_current_user` en `apis/deps.py`) y valida pertenencia antes de crear/editar (p. ej. `curso_repository.pertenece_a_usuario`).
- `GET /cursos` y `GET /horarios` solo devuelven datos del periodo activo (`PeriodoAcademico.estado = 'activo'`). El registro crea usuario + perfil + periodo inicial en una sola transacción.
- `.env` se carga desde la raíz con rutas derivadas de `__file__` (`database.py`, `core/security.py`); las variables se leen al importar, así que reinicia el servidor tras cambiarlas.
- JWT HS256 con `sub` = email; cada request vuelve a buscar el usuario activo (`estado = 1`). Contraseñas con Argon2id.
- CORS solo permite `localhost:4200` y `127.0.0.1:4200` (frontend Angular); edita `main.py` para otros orígenes.
