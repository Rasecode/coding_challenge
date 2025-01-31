# app/config.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()  # Cargar variables de entorno desde .env

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")  # Asegúrate de tener esta variable también

print("AZURE_STORAGE_CONNECTION_STRING:", AZURE_STORAGE_CONNECTION_STRING)
print("AZURE_CONTAINER_NAME:", AZURE_CONTAINER_NAME)

engine = create_engine(DATABASE_URL)
