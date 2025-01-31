# app/schemas/metrics.py
from pydantic import BaseModel
from typing import List

class HiresByDepartmentJobQuarter(BaseModel):
    department: str
    job: str
    Q1: int
    Q2: int
    Q3: int
    Q4: int

class DepartmentHiresAboveMean(BaseModel):
    id: int
    department: str
    hired: int