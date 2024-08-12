# FastAPI Task Manager

A scalable, synchronous task management API built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- **User Authentication**: Secure user authentication and authorization using JWT.
- **Task Management**: Create, update, delete, and retrieve tasks.
- **Database Migrations**: Managed with Alembic.
- **Pydantic**: Pydantic schemas utilized and Configurations are managed with Pydantic for environment variables.
- **PostgreSQL Integration**: Uses PostgreSQL as the primary database.

alembic revision --autogenerate -m "message"
alembic upgrade head

uvicorn app.main:app --reload
