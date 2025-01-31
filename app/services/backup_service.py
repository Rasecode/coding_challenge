# app/services/backup_service.py
import os
import fastavro
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.config import engine, AZURE_STORAGE_CONNECTION_STRING, AZURE_CONTAINER_NAME
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from io import BytesIO

# Configuración de Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
try:
    container_client = blob_service_client.create_container(AZURE_CONTAINER_NAME)
except ResourceExistsError:
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

def backup_table(table_name: str):
    """
    Lee todos los registros de test_api.<table_name> y los guarda en un archivo Avro
    en Azure Data Lake Storage Gen2.
    """
    output_path = f"{table_name}.avro"

    # 1) Obtener registros de la tabla
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM test_api.{table_name}"))
        raw_rows = [dict(row._mapping) for row in result]

    if not raw_rows:
        return {"message": f"No data found in test_api.{table_name}"}

    # 2) Convertir valores a str para que fastavro no falle con tipos int/float
    records = [{k: str(v) for k, v in row.items()} for row in raw_rows]

    # 3) Generar un esquema Avro, asumiendo todo "string"
    schema = {
        "type": "record",
        "name": table_name,
        "fields": [{"name": col, "type": "string"} for col in records[0].keys()]
    }

    # 4) Escribir archivo Avro en memoria
    output_stream = BytesIO()
    fastavro.writer(output_stream, schema, records)
    output_stream.seek(0)

    # 5) Subir a ADLS2
    blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=output_path)
    blob_client.upload_blob(output_stream, overwrite=True)

    return {"message": f"Backup for test_api.{table_name} saved to Azure Blob Storage as {output_path}"}

def restore_table(table_name: str):
    """
    Lee el archivo Avro desde Azure Data Lake Storage Gen2
    y re-inserta los datos en test_api.<table_name> (sin usar IDENTITY_INSERT).
    """
    avro_path = f"{table_name}.avro"
    blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=avro_path)

    try:
        download_stream = blob_client.download_blob()
        avro_data = download_stream.readall()
    except Exception as e:
        return {"message": f"Backup file not found or error downloading: {e}"}

    # 1) Leer registros Avro
    with BytesIO(avro_data) as f:
        reader = fastavro.reader(f)
        raw_rows = list(reader)

    if not raw_rows:
        return {"message": f"No records found in {avro_path}"}

    # 2) Construir Insert genérico, ya que no usamos IDENTITY
    columns = list(raw_rows[0].keys())  # Ej: ["id", "job"], etc.
    col_list = ", ".join(columns)
    param_list = ", ".join([f":{c}" for c in columns])

    insert_stmt = text(f"INSERT INTO test_api.{table_name} ({col_list}) VALUES ({param_list})")

    # 3) Insertar registros en la tabla, convirtiendo tipos si hace falta
    with Session(engine) as session:
        for row in raw_rows:
            # Convertir tipos según sea necesario
            if "id" in row:
                row["id"] = int(row["id"])
            if "amount" in row:
                row["amount"] = float(row["amount"])
            # Añadir conversiones para otros campos si es necesario

            session.execute(insert_stmt, row)
        session.commit()

    return {"message": f"Table test_api.{table_name} restored from Azure Blob Storage {avro_path}"}