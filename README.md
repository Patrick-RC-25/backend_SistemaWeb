# RandomStudy Backend

FastAPI + SQL Server mediante `pyodbc`, sin ORM. La autenticación utiliza contraseñas con Argon2id y tokens JWT.

## Configuración

1. Ejecuta `../sql/RandomStudyDB.sql` en SQL Server Management Studio.
2. Copia `.env.example` a `.env`.
3. Completa `DB_SERVER`, `DB_DATABASE`, `DB_USER`, `DB_PASSWORD`, `DB_DRIVER` y `JWT_SECRET_KEY` con valores de tu entorno. No subas `.env` al repositorio.

## Ejecutar

```powershell
uv sync
uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Documentación interactiva: http://127.0.0.1:8000/docs

## Registro

`POST /auth/register` recibe `email`, `contrasena`, `nombres`, `apellidos` y, opcionalmente, `universidad`, `carrera` y `ciclo`. Al registrar, el backend crea el usuario, el perfil y un periodo académico inicial activo.

## Recursos

Todos los recursos salvo registro/login requieren JWT Bearer. Consulta `/docs` para los esquemas completos. El listado de cursos y horarios devuelve los del periodo activo del usuario.
