#!/bin/bash

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser --email "$DJANGO_SUPERUSER_EMAIL" --noinput || true

# Start uWSGI server
uwsgi --ini uwsgi.ini
