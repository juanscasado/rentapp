#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Crear carpeta de medios si no existe
if [ ! -d "media" ]; then
  mkdir media
fi
