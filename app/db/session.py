from contextlib import contextmanager
import psycopg2
from app.core.config import settings

@contextmanager
def get_db():
    # Managed Postgres providers (Render, Neon, Supabase, Railway) usually give
    # a single DATABASE_URL. Prefer it when set, otherwise fall back to the
    # individual host/user/password/db fields (used for local development).
    if settings.DATABASE_URL:
        conn = psycopg2.connect(settings.DATABASE_URL)
    else:
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