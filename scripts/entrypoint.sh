#! /bin/bash

python manage.py migrate;
gunicorn couveflow.wsgi:application --bind 0.0.0.0:$PORT