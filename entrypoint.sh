#!/bin/sh
# Aplica las migraciones de Django
python manage.py makemigrations
python manage.py migrate


# Inicia el servicio Django
gunicorn core.wsgi:application --bind 0.0.0.0:8000 &

# Espera 10 segundos para darle tiempo al servidor Redis para iniciar
sleep 10 &

# Inicia el worker de Celery
celery -A core worker --loglevel=info &

# Inicia el beat de Celery
celery -A core beat --loglevel=info &

# Espera a que todos los servicios terminen
wait