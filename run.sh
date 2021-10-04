#!/bin/bash
python manage.py wait_for_db
python3 manage.py makemigrations core
python3 manage.py migrate
python3 manage.py createsu
# python manage.py collectstatic
# python manage.py flush
python3 manage.py runserver 0.0.0.0:8000
