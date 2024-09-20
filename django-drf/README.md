# Task Manager API (Django)

This is the **Django (DRF)** implementation of the Task Manager API.

### ⚙️ Tech Stack Used

- Django
- Django REST Framework (DRF)
- PostgreSQL
- Docker
- smtp4dev

## 🔺Development Experience

Working on the Task Manager API with Django and DRF was a rewarding journey, especially for those venturing into web development. Django, known for its "batteries-included" philosophy, offers a rich set of built-in features that make development smoother and more intuitive. The admin panel, in particular, simplifies data management and user administration, providing a great starting point for any project.

This project reinforced valuable concepts like serializers for data validation and viewsets for managing CRUD operations. Django’s ORM made database interactions straightforward, allowing us to focus more on building features rather than dealing with low-level queries.

While Django's structured approach is less flexible than some other frameworks, it provides a clear and organized foundation that facilitates efficient development and quick iterations. This structure can be very helpful, especially for those new to API development.

Overall, the Django (DRF) implementation turned out to be user-friendly and robust, making it an excellent choice for creating maintainable APIs that can adapt to various needs.

## 📦 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Amirhossein-code/Task-Manager.git
cd task-manager-api/django-drf
```

### 2. Set Up `.env` File

```text
# Django
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
