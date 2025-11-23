# Dockerfile para Django (tests y runserver)
FROM python:3.11-slim

# Evita prompts interactivos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea y usa el directorio de la app
WORKDIR /app

# Copia requirements y los instala
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia el resto del código
COPY . .

# Puerto por defecto para runserver
EXPOSE 8000

# Comando por defecto: bash (para que puedas elegir test o runserver)
CMD ["bash", "-c", "python manage.py makemigrations --noinput && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
