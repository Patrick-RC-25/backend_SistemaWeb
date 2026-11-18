"""Conexión a Microsoft SQL Server con pyodbc (sin ORM)."""

from contextlib import contextmanager
import os
from pathlib import Path
from typing import Generator

from dotenv import load_dotenv
import pyodbc

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

DB_SERVER = os.getenv("DB_SERVER", ".")
DB_PORT = os.getenv("DB_PORT", "").strip()
DB_DATABASE = os.getenv("DB_DATABASE", "RandomStudyDB")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
DB_TRUST_SERVER_CERTIFICATE = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "yes")


def get_connection_string() -> str:
    server = DB_SERVER
    if DB_PORT and "," not in server and "\\" not in server:
        server = f"{server},{DB_PORT}"
    return (
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={server};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        f"TrustServerCertificate={DB_TRUST_SERVER_CERTIFICATE};"
    )


@contextmanager
def get_db_connection() -> Generator[pyodbc.Connection, None, None]:
    conn = pyodbc.connect(get_connection_string())
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_db_cursor() -> Generator[pyodbc.Cursor, None, None]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()


def test_connection() -> bool:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    return True
