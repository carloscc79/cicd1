import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Lectura de variables de entorno con valores por defecto para desarrollo
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "app_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Inyección de dependencia para obtener sesión de BD por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()