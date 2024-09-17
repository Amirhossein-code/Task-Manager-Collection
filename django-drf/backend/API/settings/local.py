import os

from dotenv import load_dotenv

from .common import *

from .common import BASE_DIR

load_dotenv()

SECRET_KEY = "django-insecure-t4p&6eg-pcu_f938b3gtp6yi4o#e=gz-)0$kw@%$n%n$n^^s)$"

DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
ALLOWED_HOSTS = []
