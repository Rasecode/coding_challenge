# 🚀 FastAPI Dockerized Application for Data Migration & API Integration

## 📌 Project Overview

This project demonstrates how to quickly set up and run a **FastAPI application** inside a **Docker container**, designed to handle **big data migration** to a **SQL-based database system**. 

The application is built to:
- 📂 **Migrate historical data** from **CSV files** to a SQL database.
- 🔄 **Expose a REST API** for receiving new transactions in real-time.
- 🛡️ **Validate data before insertion**, ensuring compliance with business rules.
- 📦 **Support batch processing**, allowing up to **1000 transactions per request**.
- 💾 **Implement backup and restore functionality**, storing table backups in **AVRO format**.
- ☁️ **Leverage cloud storage (Azure Data Lake Storage Gen2)** for secure and scalable data management.

This solution is containerized using **Docker**, making it easy to deploy and scale across different environments.

---

## 🛠️ Features

- 🔹 **FastAPI Backend**: High-performance REST API.
- 🔹 **CSV to SQL Migration**: Moves historical data to a structured database.
- 🔹 **Real-Time Data Ingestion**: Processes new transactions via a REST API.
- 🔹 **Batch Processing**: Handles bulk inserts (1 to 1000 rows per request).
- 🔹 **Data Integrity & Validation**: Logs invalid transactions while maintaining data consistency.
- 🔹 **Backup & Restore Mechanism**: Saves tables in **AVRO format** and restores when needed.
- 🔹 **Azure Blob Storage Integration**: Securely stores backups in **Azure Data Lake Storage Gen2 (ADLS2)**.
- 🔹 **Dockerized Deployment**: Simplifies execution and cloud integration.
- 🔹 **JWT Authentication**: Uses **HS256** for secure API access.

---

## 📌 Prerequisites

Before running this application, ensure you have the following resources created:

### **1️⃣ Azure SQL Database**
- A **SQL-based database** for storing both migrated and incoming data.
- Required details:
  - **Database Host** (e.g., `your-database.database.windows.net`)
  - **Database Name** (e.g., `your_db_name`)
  - **Username & Password** for authentication.
  - **ODBC Driver** installed (see troubleshooting section).

### **2️⃣ Azure Data Lake Storage Gen2 (ADLS2)**
- Required for **storing backups** in **AVRO format**.
- Needed details:
  - **Storage Account Name**
  - **Container Name**
  - **Storage Connection String**

### **3️⃣ Software Requirements**
- **Python 3.11** or later
- **Docker** installed
- **Azure CLI** (optional but recommended)

---

## ⚙️ How the Application Works

1. **Data Migration**  
   - Reads **historical data from CSV files**.
   - Validates transactions based on **predefined rules**.
   - Inserts valid data into the **SQL database**, while logging invalid transactions.

2. **REST API for Data Ingestion**  
   - Accepts new transactions via **FastAPI-based API**.
   - Supports **batch processing** of up to **1000 rows per request**.
   - Ensures **data integrity**, rejecting non-compliant transactions.

3. **Backup & Restore Mechanism**  
   - Creates **periodic backups** in **AVRO format**.
   - Saves backups in **Azure Data Lake Storage Gen2**.
   - Allows **restoration of specific tables** from backups.

Once everything is set up, the API documentation is available at:  
🔹 **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📌 Step 1: Clone the Repository

```sh
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## Step 2: Create and Set Up a Python Virtual Environment

Once inside the project folder, create a virtual environment for Python 3.11 and activate it:

```sh
python3 -m venv env_migration
source env_migration/bin/activate  
```

# On macOS/Linux

## Step 3: Install Dependencies

Install the necessary dependencies via pip using the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

Ensure you have an `.env` file in the root directory with the following environment variables:

```ini
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your_account_name;AccountKey=your_account_key;EndpointSuffix=core.windows.net
AZURE_CONTAINER_NAME=your_container_name
DATABASE_URL=mssql+pyodbc://your_db_user:your_db_password@your_db_host:1433/your_db_name?driver=ODBC+Driver+18+for+SQL+Server
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://your_redis_host:6379
```

# Optional

## Step 5: Build the Docker Image

The next step is to build the Docker image. Make sure you are in the root directory of your project where the `Dockerfile` is located. The image will be built with the necessary dependencies and configurations.

Run the following command to build the Docker image:

```sh
docker build --platform linux/amd64 -t fastapi-app:v1 .
```

## Step 6: Run the Docker Container

Once the Docker image is built, you can run it locally in a container. This will map port `8000` from the container to port `8000` on your local machine, so you can access the application through your browser or API testing tools.

Run the following command to start the container:

```sh
docker run -d --name fastapi-app -p 8000:8000 --env-file .env fastapi-app:v1
```

## Step 7: Verify the Application is Running

Once the container is running, open a web browser or use an API testing tool (e.g., Postman or `curl`) to check the status of the FastAPI application.

You should be able to access the application at:

🔹 **FastAPI application URL:**  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

🔹 **OpenAPI documentation:**  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## Step 8: Troubleshooting

If you encounter any issues, the most common errors are related to missing dependencies or configuration issues. Here are some potential fixes:

### 1. Missing ODBC Driver  
If the application fails to connect to the database due to the ODBC driver not being found, you can install it using the following commands:

#### macOS:
```sh
brew install --no-sandbox msodbcsql18
```

#### Linux (Ubuntu/Debian):
```sh
sudo apt-get install unixodbc-dev
```

### 2. Database Connection Issues  
Double-check your database credentials and ensure the database is accessible from within the Docker container.


## Step 9: Dockerize the Application for Production

If you wish to deploy this FastAPI application to production, you can use the Docker image as is, or integrate it into a larger deployment pipeline. You can deploy the image to cloud platforms like **Azure**, **AWS**, or **Google Cloud**, or run it on your own infrastructure.


## Conclusion

This project demonstrates how to quickly get a FastAPI application running locally in a Docker container. The FastAPI app connects to a **SQL Server** database using `pyodbc` and can also interact with **Azure Blob Storage** for backups. The Dockerized setup allows for easy testing and deployment in various environments.

This `README.md` contains the full setup process and details the steps from the beginning to running the FastAPI application locally inside a Docker container. You can copy and paste it directly into your repository's README file.