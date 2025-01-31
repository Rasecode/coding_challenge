import pandas as pd
import os
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import engine

def load_departments_csv(file_path: str):
    df = pd.read_csv(file_path, header=None)
    # Estructura: id, department
    if df.shape[1] != 2:
        print(f"❌ Estructura inválida en {file_path}, se esperaban 2 columnas")
        return

    df.columns = ["id", "department"]
    _process_departments(df)

def load_jobs_csv(file_path: str):
    df = pd.read_csv(file_path, header=None)
    # Estructura: id, job
    if df.shape[1] != 2:
        print(f"❌ Estructura inválida en {file_path}, se esperaban 2 columnas")
        return

    df.columns = ["id", "job"]
    _process_jobs(df)

def load_hired_employees_csv(file_path: str):
    df = pd.read_csv(file_path, header=None)
    # Estructura: id, name, datetime, department_id, job_id
    if df.shape[1] != 5:
        print(f"❌ Estructura inválida en {file_path}, se esperaban 5 columnas")
        return

    df.columns = ["id", "name", "datetime", "department_id", "job_id"]
    _process_hired_employees(df)

# ---------------------------------------------------
# Funciones internas que insertan datos en la BD (sin usar IDENTITY_INSERT)
# ---------------------------------------------------

def _process_departments(df):
    from app.models.models import Department
    with Session(engine) as session:
        for idx, row in df.iterrows():
            # Todos los campos son requeridos, valida que no estén vacíos
            if pd.isnull(row["id"]) or pd.isnull(row["department"]):
                print(f"❌ Fila inválida (campos requeridos vacíos): {row}")
                continue

            try:
                dep = Department(
                    id=int(row["id"]),  # Tablas sin IDENTITY => se puede insertar ID libremente
                    department=str(row["department"]).strip()
                )
                session.add(dep)
            except Exception as e:
                print(f"❌ Error procesando fila {row}: {e}")

        session.commit()

def _process_jobs(df):
    from app.models.models import Job
    with Session(engine) as session:
        for idx, row in df.iterrows():
            if pd.isnull(row["id"]) or pd.isnull(row["job"]):
                print(f"❌ Fila inválida (campos requeridos vacíos): {row}")
                continue

            try:
                job = Job(
                    id=int(row["id"]),
                    job=str(row["job"]).strip()
                )
                session.add(job)
            except Exception as e:
                print(f"❌ Error procesando fila {row}: {e}")

        session.commit()

def _process_hired_employees(df):
    from app.models.models import HiredEmployee
    with Session(engine) as session:
        for idx, row in df.iterrows():
            # Todos los campos son requeridos
            if any(pd.isnull(row[col]) for col in ["id", "name", "datetime", "department_id", "job_id"]):
                print(f"❌ Fila inválida (campos requeridos vacíos): {row}")
                continue

            try:
                he = HiredEmployee(
                    id=int(row["id"]),  # De nuevo, sin IDENTITY => se inserta directo
                    name=str(row["name"]).strip(),
                    datetime=str(row["datetime"]).strip(),
                    department_id=int(row["department_id"]),
                    job_id=int(row["job_id"])
                )
                session.add(he)
            except Exception as e:
                print(f"❌ Error procesando fila {row}: {e}")

        session.commit()