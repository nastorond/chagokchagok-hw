#!/bin/sh

python -m venv venv
source venv/bin/activate
pip install -r server-requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 172.19.0.4:8081