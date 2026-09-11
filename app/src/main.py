from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from .database import get_db, Base, engine
from . import models, schemas

# Creación automática de tablas al iniciar (para la demo)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Demo CI/CD API - Desarrollo y Nuevas Tecnologías",
    version="1.0.0"
)

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoring"])
def healthcheck(db: Session = Depends(get_db)):
    """
    Endpoint de Salud (Healthcheck) para el pipeline de CI/CD.
    Valida la conectividad viva con la base de datos PostgreSQL.
    """
    try:
        # Ejecuta un 'ping' SQL para confirmar que la BD responda
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "service": "api-web"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )

@app.get("/api/v1/items", response_model=List[schemas.ItemResponse], tags=["Items"])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Lista los ítems registrados en el sistema."""
    return db.query(models.SystemItem).offset(skip).limit(limit).all()

@app.post("/api/v1/items", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Crea un nuevo ítem en la base de datos."""
    db_item = models.SystemItem(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item