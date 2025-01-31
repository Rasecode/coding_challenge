# app/routes/metrics.py
from fastapi import APIRouter, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from app.schemas.metrics import HiresByDepartmentJobQuarter, DepartmentHiresAboveMean
from app.models.models import Department, Job, HiredEmployee
from app.config import engine

router = APIRouter()

@router.get("/metrics/hires-by-department-job-quarter", response_model=List[HiresByDepartmentJobQuarter])
def get_hires_by_department_job_quarter():
    """
    Número de empleados contratados por cada trabajo y departamento en 2021, dividido por trimestre.
    """
    with Session(engine) as session:
        results = (
            session.query(
                Department.department,
                Job.job,
                func.sum(
                    case(
                        (extract('quarter', HiredEmployee.datetime) == 1, 1),
                        else_=0
                    )
                ).label("Q1"),
                func.sum(
                    case(
                        (extract('quarter', HiredEmployee.datetime) == 2, 1),
                        else_=0
                    )
                ).label("Q2"),
                func.sum(
                    case(
                        (extract('quarter', HiredEmployee.datetime) == 3, 1),
                        else_=0
                    )
                ).label("Q3"),
                func.sum(
                    case(
                        (extract('quarter', HiredEmployee.datetime) == 4, 1),
                        else_=0
                    )
                ).label("Q4"),
            )
            .join(Job, HiredEmployee.job_id == Job.id)
            .join(Department, HiredEmployee.department_id == Department.id)
            .filter(func.year(HiredEmployee.datetime) == 2021)
            .group_by(Department.department, Job.job)
            .order_by(Department.department.asc(), Job.job.asc())
            .all()
        )

        # Transformar los resultados en una lista de diccionarios
        hires_list = [
            HiresByDepartmentJobQuarter(
                department=row.department,
                job=row.job,
                Q1=row.Q1,
                Q2=row.Q2,
                Q3=row.Q3,
                Q4=row.Q4
            )
            for row in results
        ]

        return hires_list

@router.get("/metrics/departments-hires-above-mean", response_model=List[DepartmentHiresAboveMean])
def get_departments_hires_above_mean():
    """
    Lista de IDs, nombres y número de empleados contratados de cada departamento que hayan contratado
    más empleados que el promedio de todos los departamentos en 2021, ordenado de manera descendente.
    """
    with Session(engine) as session:
        # Calcular el total de contrataciones por departamento en 2021
        dept_hires = (
            session.query(
                Department.id,
                Department.department,
                func.count(HiredEmployee.id).label("hired")
            )
            .join(HiredEmployee, HiredEmployee.department_id == Department.id)
            .filter(func.year(HiredEmployee.datetime) == 2021)
            .group_by(Department.id, Department.department)
            .subquery()
        )

        # Calcular la media de contrataciones
        mean_hires = session.query(func.avg(dept_hires.c.hired)).scalar()

        # Filtrar departamentos que superen la media
        results = (
            session.query(
                dept_hires.c.id,
                dept_hires.c.department,
                dept_hires.c.hired
            )
            .filter(dept_hires.c.hired > mean_hires)
            .order_by(dept_hires.c.hired.desc())
            .all()
        )

        # Transformar los resultados en una lista de diccionarios
        hires_above_mean = [
            DepartmentHiresAboveMean(
                id=row.id,
                department=row.department,
                hired=row.hired
            )
            for row in results
        ]

        return hires_above_mean