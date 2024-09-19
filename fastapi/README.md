# Task Manager API (FastAPI)

This is the **FastAPI** implementation of the Task Manager API.

## Features

- **User Authentication**: JWT-based stateless authentication with email and password.
- **Password Reset** : Users can reset their password via their email
- **Task Management**: Users can create, view, update, and delete tasks. Each task is owned by a specific user and only accessible by them.
- **Task Categorization**: Users can create categories and sort their tasks

## Tech Stack

- **FastAPI**
- **Pydantic**
- **SQLAlchemy**
- **Alembic**
- **Docker**
- **Async development**
- **smtp4dev**
- **pgadmin4**

## Installation and Setup

### 1. Clone the repository:

```bash
git clone https://github.com/Amirhossein-code/Task-Manager.git
cd task-manager-api/fastapi
```

### 2. Set Up `.env` File Values

We will create two environment files: `.env` and `.env.docker`. because pydantic settings complains if there are env in .env but not in the classes fields so we create a new .env to bypass

#### 1. **.env File**

This file contains the environment variables needed by your FastAPI application. The content should look like this:

```text
# Database connection
DATABASE_URL=postgresql+asyncpg://<postgres_user>:<postgres_pass>@db:5432/task_manager_db

# Security settings
SECRET_KEY=bew_secret_key
ALGORITHM=HS256

# Token expiration
ACCESS_TOKEN_EXPIRE_MINUTES=30
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES=5

# SQLAlchemy settings
ECHO_SQL=True

# SMTP4DEV
SMTP_SERVER=smtp4dev
SMTP_PORT=25
SENDER_EMAIL=noreply@example.com
RESET_CALLBACK_URL=http://0.0.0.0:8000/reset-password
```

#### 1. **.env.docker File**

This file is used by Docker services like PostgreSQL, PgAdmin, and SMTP4dev. The content should look like this:

```text
# Database connection
POSTGRES_DB=task_manager_db
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_pass>
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
- pgAdmin: `http://localhost:5050` (Login with admin@example.com / password)
- smtp4dev: `http://localhost:3000` (Login with admin / password)

## Dev Experience

Building the Task Manager API with FastAPI was a rewarding experience, especially for a developer transitioning from Django/DRF. The flexibility and speed of FastAPI provided a fresh approach to development, despite its more minimalistic structure compared to Django.

Key learnings included mastering dependency injection, adapting to Pydantic for data validation, and working with SQLAlchemy and Alembic for database interactions. The project went through several refactoring cycles, leading to a clean, scalable structure.

Overall, FastAPI proved to be fast, lightweight, and highly extensible, making it an excellent framework for building modern, maintainable APIs.

## Contributing

Thank you for your interest in contributing to the Task Manager API (FastAPI-sync)! This project aims to provide a foundational API with essential features like user authentication, CRUD operations for users, and basic task management. It serves as a starting point for a FastAPI-based application, incorporating simple authentication, user management, and task functionality. If you'd like to contribute to this project, please feel free to fork the repository, create a branch, and submit a pull request. Any contributions are welcome!
