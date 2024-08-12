# Task Manager API Collection

This repository contains a collection of task management API implementations using various frameworks and approaches. The goal is to provide a comprehensive comparison and demonstrate best practices across different technologies.

## Implementations

### 1. Django REST Framework (DRF)
- **Framework**: Django with Django REST Framework.
- **Database**: PostgreSQL.
- **Features**:
  - User authentication and authorization.
  - CRUD operations for tasks.
  - Token-based authentication using JWT.

### 2. FastAPI (Synchronous)
- **Framework**: FastAPI.
- **Database**: PostgreSQL with SQLAlchemy.
- **Features**:
  - Synchronous API endpoints.
  - User authentication and authorization using JWT.
  - Task management with Alembic-managed database migrations.
  - Configuration management with Pydantic.

<!-- ### 3. FastAPI (Asynchronous) _(Coming Soon)_
- **Framework**: FastAPI (Async).
- **Database**: PostgreSQL with SQLAlchemy (Async).
- **Planned Features**:
  - Fully asynchronous API endpoints.
  - Asynchronous database operations with SQLAlchemy.
  - Optimized for performance and scalability. -->
