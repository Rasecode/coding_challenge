# app/routes/backups.py
from fastapi import APIRouter, HTTPException
from app.services.backup_service import backup_table, restore_table

router = APIRouter()

@router.post("/backup/{table_name}")
def backup(table_name: str):
    try:
        result = backup_table(table_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/restore/{table_name}")
def restore(table_name: str):
    try:
        result = restore_table(table_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))