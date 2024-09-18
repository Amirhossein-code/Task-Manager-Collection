# Task Manager API (FastAPI-Async)

This is the **FastAPI** implementation of the Task Manager API. This application handles user authentication and task management using **JWT tokens** with **stateless** authentication. Each user has control over their own tasks, ensuring that tasks remain private and secure.

## Features

- **User Authentication**: JWT-based authentication with username and password.
- **Task Management**: Users can create, view, update, and delete tasks. Each task is owned by a specific user and only accessible by them.
- **SQLAlchemy ORM**: Handles database interactions.
- **Alembic Migrations**: Manages database migrations.
- **Pydantic Validation**: Used for data validation and serialization.
- **Dockerized**: The entire app is containerized using Docker for easy setup and deployment.

## Requirements

- **Docker**: The app is fully containerized.
- **FastAPI**: High-performance web framework.
- **SQLAlchemy**: ORM for database interactions.
- **Alembic**: Handles database migrations.
- **Pydantic**: Used for validation and serialization.

## Installation and Setup

### 1. Clone the repository:

```bash
git clone https://github.com/Amirhossein-code/Task-Manager.git
cd task-manager-api/fastapi-sync
```

### 2. Set Up `.env` File Values

We will create two environment files: `.env` and `.env.docker`.

#### 1. **.env File**

This file contains the environment variables needed by your FastAPI application. The content should look like this:

```text
# Database connection
DATABASE_URL=postgresql://<postgres_user>:<postgres_password>@db:<postgres_port>/<postgres_db>

# Security settings
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256

# Token expiration
ACCESS_TOKEN_EXPIRE_MINUTES=30

# SQLAlchemy settings
ECHO_SQL=True

# Testing mode
TEST=False
```

#### 1. **.env.docker File**

This file is used by Docker services like PostgreSQL, PgAdmin, and SMTP4dev. The content should look like this:

```text
# Database connection
POSTGRES_DB=your_database_name
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# PgAdmin settings
PGADMIN_DEFAULT_EMAIL=admin@email.com
PGADMIN_DEFAULT_PASSWORD=password

# SMTP4dev settings
SMTP4DEV_ADMIN_USERNAME=admin
SMTP4DEV_ADMIN_PASSWORD=password
```

**Note:** You can generate a secret key with the following command:

```bash
openssl rand -hex 32
```

### 3. Run the application with Docker Compose:

```bash
docker compose up --build
```

### 4. Access the application:

- FastAPI Swagger UI: `http://localhost:8000/docs`
- pgAdmin: `http://localhost:5050` (Login with admin@example.com / admin)
