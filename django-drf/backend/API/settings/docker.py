import os

from dotenv import load_dotenv

from .common import *
from .common import BASE_DIR

load_dotenv()


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-)hf=%kwj)utr&6!*k)#kq^o5by0=8i45#r7%u!o53)dcldx7a_",
)

DEBUG = False


# Function to check if PostgreSQL credentials are set
def is_postgres_configured():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    return user is not None and password is not None


# Set up the DATABASES configuration
if is_postgres_configured():
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST", "db"),
            "PORT": os.getenv("POSTGRES_PORT", 5432),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),  # Path to SQLite database
        }
    }


ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split(" ")

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]
