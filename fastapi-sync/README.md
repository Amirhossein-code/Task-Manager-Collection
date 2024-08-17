# Task Manager API (FastAPI-sync)

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

### 2. update .env file values

A sample .env file is provided in the project folder. Update the values for your use case. You can generate a new secret key with the following command:

```bash
openssl rand -hex 32
```

Be sure to update other values like the PostgreSQL credentials and host information.

### 3. Run the application with Docker Compose:

```bash
docker-compose up --build
```

### 4. Access the application:

- FastAPI Swagger UI: `http://localhost:8000/docs`
- pgAdmin: `http://localhost:5050` (Login with admin@example.com / admin)

## Testing

The project includes comprehensive integration tests using pytest, achieving over 90% test coverage. The remaining 10% of the code primarily covers logging and handling edge-case exceptions. These parts are designed to manage unexpected scenarios and ensure proper logging, though they don't directly impact the core business logic. Since these scenarios are challenging to reproduce in typical conditions, However, they are crucial for robust error handling and logging. Testing these components is possible if needed, but the primary focus remains on verifying core functionality.

### Running the tests:

#### 1. access the application container:

```bash
docker exec -it task_manager_app sh
```

#### 2. Run the tests:

```bash
pytest
```

## Developer Experience

Building the Task Manager API with FastAPI was a rewarding experience, especially for a developer transitioning from Django/DRF. The flexibility and speed of FastAPI provided a fresh approach to development, despite its more minimalistic structure compared to Django.

Key learnings included mastering dependency injection, adapting to Pydantic for data validation, and working with SQLAlchemy and Alembic for database interactions. The project went through several refactoring cycles, leading to a clean, scalable structure.

Overall, FastAPI proved to be fast, lightweight, and highly extensible, making it an excellent framework for building modern, maintainable APIs.

## Contributing

Thank you for your interest in contributing to the Task Manager API (FastAPI-sync)! This project aims to provide a foundational API with essential features like user authentication, CRUD operations for users, and basic task management. It serves as a starting point for a FastAPI-based application, incorporating simple authentication, user management, and task functionality. If you'd like to contribute to this project, please feel free to fork the repository, create a branch, and submit a pull request. Any contributions are welcome!
