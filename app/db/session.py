from contextlib import contextmanager
import psycopg2
from app.core.config import settings

@contextmanager
def get_db():
    conn = psycopg2.connect(
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT
    )
    try:
        yield conn
    finally:
        conn.close() 