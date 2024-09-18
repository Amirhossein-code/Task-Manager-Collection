# ⚖️ Task Manager API

### 🔺 Description

The Task Manager API is a RESTful application that allows users to efficiently manage their tasks. Users can create, categorize, and manage tasks, ensuring their workloads are organized and manageable. This API also includes secure user authentication and password reset functionality.

### 🔺 Features

- **Task Management:** Define tasks based on individual requirements and categorize them.
- **User Authentication:** Secure login and sign-up using email and password credentials.
- **Resetting Password:** Reset passwords via email.

### ⚙️ Tech Stack Used

Python, Django, Django Rest Framework, Smtp4dev, Docker, PostgreSQL

### 📦 Getting Started

#### 1. Clone the repo

```bash
git clone https://github.com/Amirhossein-code/Task-Manager.git
cd task-manager-api/django-drf
```

### 2. Set Up `.env` File

```text
# Djnago
SECRET_KEY=secret_key
DJANGO_ALLOWED_HOSTS=localhost

# DataBase
POSTGRES_DB=postgres_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# SMTP4dev
SMTP4DEV_ADMIN_USERNAME=admin
SMTP4DEV_ADMIN_PASSWORD=pass12345


# PgAdmin
PGADMIN_DEFAULT_EMAIL=admin@email.com
PGADMIN_DEFAULT_PASSWORD=12345

```

**Note:** You can get a new secret key from `https://djecrety.ir/`

### 3. Run the application with Docker Compose:

```bash
docker compose up --build
```
