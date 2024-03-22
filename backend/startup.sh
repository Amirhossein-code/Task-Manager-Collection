#!/bin/bash

python manage.py makemigrations
python manage.py migrate

# Create superuser non-interactively
python manage.py createsuperuser --email 12@gmail.com

python manage.py seed

python manage.py runserver
