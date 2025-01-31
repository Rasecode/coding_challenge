# app/routes/transactions.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import pandas as pd
from io import StringIO  # Importa StringIO desde el módulo io

from app.services.csv_loader import (
    load_departments_csv,
    load_jobs_csv,
    load_hired_employees_csv
)

router = APIRouter()

@router.post("/upload-departments")
def upload_departments(file: UploadFile = File(...)):
    try:
        # Leer el contenido del archivo en memoria
        contents = file.file.read().decode("utf-8")
        df = pd.read_csv(StringIO(contents), header=None)  # Usar StringIO de io

        # Verificar el número de filas
        num_rows = df.shape[0]
        if num_rows < 1 or num_rows > 1000:
            raise HTTPException(
                status_code=400,
                detail=f"El número de filas debe estar entre 1 y 1000. Se recibieron {num_rows} filas."
            )

        # Guardar el archivo
        file_path = f"app/data/{file.filename}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(contents)

        # Procesar el CSV
        load_departments_csv(file_path)
        return {"message": "Departments CSV uploaded and processed successfully."}

    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Archivo CSV inválido.")
    finally:
        file.file.close()

@router.post("/upload-jobs")
def upload_jobs(file: UploadFile = File(...)):
    try:
        # Leer el contenido del archivo en memoria
        contents = file.file.read().decode("utf-8")
        df = pd.read_csv(StringIO(contents), header=None)  # Usar StringIO de io

        # Verificar el número de filas
        num_rows = df.shape[0]
        if num_rows < 1 or num_rows > 1000:
            raise HTTPException(
                status_code=400,
                detail=f"El número de filas debe estar entre 1 y 1000. Se recibieron {num_rows} filas."
            )

        # Guardar el archivo
        file_path = f"app/data/{file.filename}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(contents)

        # Procesar el CSV
        load_jobs_csv(file_path)
        return {"message": "Jobs CSV uploaded and processed successfully."}

    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Archivo CSV inválido.")
    finally:
        file.file.close()

@router.post("/upload-hired-employees")
def upload_hired_employees(file: UploadFile = File(...)):
    try:
        # Leer el contenido del archivo en memoria
        contents = file.file.read().decode("utf-8")
        df = pd.read_csv(StringIO(contents), header=None)  # Usar StringIO de io

        # Verificar el número de filas
        num_rows = df.shape[0]
        if num_rows < 1 or num_rows > 1000:
            raise HTTPException(
                status_code=400,
                detail=f"El número de filas debe estar entre 1 y 1000. Se recibieron {num_rows} filas."
            )

        # Guardar el archivo
        file_path = f"app/data/{file.filename}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(contents)

        # Procesar el CSV
        load_hired_employees_csv(file_path)
        return {"message": "Hired Employees CSV uploaded and processed successfully."}

    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Archivo CSV inválido.")
    finally:
        file.file.close()