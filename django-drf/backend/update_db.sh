#!/bin/bash

python manage.py makemigrations app
python manage.py makemigrations individual
python manage.py makemigrations core

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
