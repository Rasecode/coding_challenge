# app/models/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class HiredEmployee(Base):
    __tablename__ = "hired_employees"
    # Supongamos que tu esquema es "test_api"
    __table_args__ = {"schema": "test_api"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    datetime = Column(String, nullable=False)  # Podrías convertir a DATETIME si deseas
    department_id = Column(Integer, nullable=False)
    job_id = Column(Integer, nullable=False)

class Department(Base):
    __tablename__ = "departments"
    __table_args__ = {"schema": "test_api"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    department = Column(String, nullable=False)

class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = {"schema": "test_api"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    job = Column(String, nullable=False)

print("DEBUG: Definiendo Job")    