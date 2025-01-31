# app/main.py
from fastapi import FastAPI
from app.routes import transactions, backups, metrics  # Asegúrate de importar metrics

app = FastAPI()

# Incluir los routers existentes
app.include_router(transactions.router)
app.include_router(backups.router)
app.include_router(metrics.router)  # Incluir el router de métricas