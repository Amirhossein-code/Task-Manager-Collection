from .common import *
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = "django-insecure-t4p&6eg-pcu_f938b3gtp6yi4o#e=gz-)0$kw@%$n%n$n^^s)$"

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "mysql.connector.django",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST_LOCAL"),
        "PORT": os.environ.get("DB_PORT_LOCAL"),
    }
}
