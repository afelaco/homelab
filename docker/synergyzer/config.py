import os
from sqlalchemy import create_engine

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mysecretpassword")
POSTGRES_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@host.docker.internal:5432/postgres"

def get_engine():
    """Creates and returns the SQLAlchemy database engine."""
    return create_engine(POSTGRES_URL)