# Task Manager API

This is the **FastAPI** implementation of the Task Manager API

## Tech Stack

- **FastAPI**: Asynchronous web framework for building APIs with Python.
- **Pydantic**: For data validation and settings management.
- **SQLAlchemy**: ORM for database interactions.
- **Alembic**: Database migration tool.
- **PostgreSQL**: For persistent storage of tasks, users, and categories.
- **Docker**: For containerizing the application.
- **smtp4dev**: For email testing during development.

## Development Experience

Working on the Task Manager API with FastAPI was both rewarding and refreshing, especially transitioning from Django/DRF. FastAPI’s flexibility provided a new approach, with its more minimalistic structure offering a contrast to Django’s built-in features.

This project reinforced important concepts like dependency injection, Pydantic for data validation, asynchronous development, and integrating SQLAlchemy with Alembic for database migrations. After several rounds of refactoring, we established a clean and scalable architecture.

FastAPI's async support made it effortless to handle concurrent requests, significantly improving performance. Additionally, the automatic API documentation via Swagger and Redoc was a huge plus, providing interactive, real-time docs without extra setup.

Overall, FastAPI proved to be lightweight, fast, and highly suited for building modern APIs that are easy to maintain and scale.

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
