# FastAPI Application with Docker

This project demonstrates how to run a FastAPI application using Docker. The application is designed to perform specific database operations and expose endpoints through FastAPI. It is connected to a Microsoft SQL Server database and uses Azure Blob Storage for backups.

## Project Setup and Instructions

### Prerequisites

Before starting, ensure you have the following installed on your local machine:

- **Docker**: For containerizing and running the FastAPI application in a container.
- **Python 3.11**: For setting up the development environment and dependencies.
- **SQL Server ODBC Driver**: The application connects to SQL Server using `pyodbc`.

### Step 1: Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/your-repository-url
cd your-repository-folder
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