# Task Manager API

This is the **FastAPI** implementation of the Task Manager API, designed for managing user tasks efficiently with robust features and a modern tech stack.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#installation-and-setup)
- [Development Experience](#)

## Overview

The Task Manager API provides a platform for users to manage their tasks. It implements user authentication, task management features, and categorization, aiming to streamline task handling and enhance productivity.

## Features

- **User Authentication**: Implements JWT-based stateless authentication using email and password for secure access.
- **Password Reset**: Facilitates password recovery via email, enabling users to reset their passwords seamlessly.
- **Task Management**: Users can create, view, update, and delete tasks. Each task is uniquely associated with a specific user, ensuring privacy and data integrity.
- **Task Categorization**: Users can create task categories, allowing them to sort and filter their tasks efficiently.

## Tech Stack

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Pydantic**: For data validation and settings management using Python type annotations.
- **SQLAlchemy**: The SQL toolkit and ORM for Python, facilitating easy database interactions.
- **Alembic**: A lightweight database migration tool for use with SQLAlchemy.
- **Docker**: For containerizing the application, ensuring consistent environments across development and production.
- **Asynchronous Development**: Utilizing Python’s `async` and `await` features for non-blocking I/O operations to enhance performance.
- **smtp4dev**: A simple SMTP server designed for testing emails during development.
- **pgAdmin4**: A web-based GUI for managing PostgreSQL databases, allowing for cleaner database management and monitoring.

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

