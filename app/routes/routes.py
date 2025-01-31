from fastapi import APIRouter
from sqlalchemy import text
from app.config import engine

router = APIRouter()

@router.get("/test-db")
def test_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 AS Prueba"))
        data = [dict(row._mapping) for row in result]
        return {"db_result": data}

@router.get("/")
def root():
    return {"message": "Bienvenido a mi API"}