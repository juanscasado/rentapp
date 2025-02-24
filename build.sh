export DJANGO_SUPERUSER_NAME=myadmin
export DJANGO_SUPERUSER_EMAIL=myadmin@example.com
export DJANGO_SUPERUSER_PASSWORD=securepassword
./build.sh#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
#!/bin/sh

# Aplica migraciones
python manage.py migrate

# Crear superusuario sin entrada manual
SUPERUSER_NAME=${DJANGO_SUPERUSER_NAME:-admin}
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-adminpassword}

echo "from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$SUPERUSER_NAME').exists():
    User.objects.create_superuser('$SUPERUSER_NAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell

echo "from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'juans.casado@gmail.com', 'adminpassword')" | python manage.py shell
