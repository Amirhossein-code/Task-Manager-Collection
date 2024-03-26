from .common import *
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = "django-insecure-t4p&6eg-pcu_f938b3gtp6yi4o#e=gz-)0$kw@%$n%n$n^^s)$"

DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

ALLOWED_HOSTS = []
