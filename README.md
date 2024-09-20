# Task Manager API Collection

## Description

This repository is a simple guide to building a Task Manager API using a variety of web frameworks. It's designed for developers who want to experiment with different technologies while keeping things approachable. Each implementation focuses on the basics, without overwhelming you with unnecessary complexity.

By comparing these implementations, you'll get a good sense of how common tasks like user authentication and task management are handled differently in various frameworks. The idea is to learn by doing!

## Implementations

### **[1. Django (DRF)](django-drf/README.md)**

The FastAPI implementation focuses on performance and simplicity. It utilizes Python's async capabilities and type hints to create a high-performance API with minimal code. This implementation showcases how FastAPI’s asynchronous nature allows for efficient handling of concurrent tasks, making it ideal for scalable applications.

### **[2. FastAPI](fastapi/README.md)**

The FastAPI implementation focuses on performance and simplicity. It utilizes Python's async capabilities and type hints to create a high-performance API with minimal code. This implementation showcases how FastAPI’s asynchronous nature allows for efficient handling of concurrent tasks, making it ideal for scalable applications.

## Minimal Task Manager API

Each implementation of the Task Manager API includes the following core features:

- **User Authentication:** Secure login, registration, and token-based authentication (JWT).
- **Task Management:** CRUD (Create, Read, Update, Delete) operations for tasks, allowing users to manage their tasks.
- **Task Categorization:** Ability for users to organize tasks by assigning them to categories.
- **Password Reset:** Users should be able to reset their passwords via email (using smtp4dev for development).
- **PostgreSQL:** The database for persistent storage of users, tasks, and categories.
- **Dockerized Deployment:** The entire application is containerized using Docker, ensuring a consistent and reproducible development and production environment.
