# RentApp

Guía rápida para instalar, configurar y ejecutar la aplicación y las pruebas en local (Windows / PowerShell).

Requisitos
- Python 3.12
- Git
- (Opcional) Cuenta Gmail para SMTP con "App password" si quieres enviar emails reales

Instalación local (PowerShell)
1. Ir al proyecto
   ```
   cd C:\Users\WinFree\Desktop\repo\rentapp
   ```

2. Crear y activar el entorno virtual
   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Instalar dependencias
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

Configurar variables de entorno (.env)
1. Copia el template y edítalo localmente (NO subir .env al repo)
   ```
   copy .env.example .env
   notepad .env
   ```
2. Generar una SECRET_KEY segura:
   ```
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Pegar en `SECRET_KEY` dentro de `.env`.

3. Ejemplo para SMTP con Gmail (usar app password):
   ```
   EMAIL_HOST_USER=tu_email@gmail.com
   EMAIL_HOST_PASSWORD=tu_app_password
   DEFAULT_FROM_EMAIL=tu_email@gmail.com
   SECRET_KEY=<la_clave_generada>
   DEBUG=True
   ```

Asegurar que .env está ignorado por git
```
echo ".env" >> .gitignore
git add .gitignore
git commit -m "chore: ignore local .env"
```

Migraciones y archivos estáticos
```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

Crear superusuario (opcional)
```
python manage.py createsuperuser
```

Levantar servidor local
```
python manage.py runserver
# visitar http://127.0.0.1:8000/
```

Ejecutar pruebas (usando el test runner de Django) — recomendado
```
python manage.py test rentapp --verbosity 2
```
Desde docker
```
docker run --rm rentapp python manage.py test rentapp.tests.test_models rentapp.tests.test_views
```

Despliegue en Render
Ver guía completa en [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

Resumen rápido:
1. Configura las variables de entorno en Render:
   - `SECRET_KEY` (genera una nueva con el comando en la guía)
   - `DEBUG=False`
   - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` (Gmail)
   - Opcionalmente: `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`

2. Build Command en Render: `./build.sh`

3. Start Command: `gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 3`

4. Push a main:
   ```
   git add .
   git commit -m "fix: configuración para Render"
   git push origin main
   ```

5. En Render: "Manual Deploy" → "Clear build cache & deploy"

Seguridad
- Nunca subir `.env` ni contraseñas al repositorio.
- Si una app password o secreto queda expuesto: revoca y regenera inmediatamente.
- Mantén `SECRET_KEY` fuera del control de versiones.

Fin.

---

# Uso con Docker

## Construir la imagen
```powershell
docker build -t rentapp .
```

## Aplicar migraciones (solo la primera vez o tras cambios en modelos)
```powershell
docker run --rm rentapp python manage.py makemigrations --noinput
docker run --rm rentapp python manage.py migrate --noinput
```

## Ejecutar los tests
```powershell
docker run --rm rentapp python manage.py test rentapp.tests.test_models rentapp.tests.test_views
```

## Levantar el servidor en el puerto 8000
```powershell
docker run -p 8000:8000 rentapp python manage.py runserver 0.0.0.0:8000
```

## (Opcional) Ejecutar migraciones y servidor automáticamente
Puedes modificar el Dockerfile para que el contenedor ejecute migraciones y luego levante el servidor automáticamente:

```
CMD ["bash", "-c", "python manage.py makemigrations --noinput && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
```

Así solo necesitas:
```powershell
docker build -t rentapp .
docker run -p 8000:8000 rentapp
```

Para detener el contenedor que está corriendo en primer plano (por ejemplo, con el servidor Django), simplemente presiona Ctrl+C en la terminal donde lo ejecutaste.

Si el contenedor está corriendo en segundo plano (con -d), usa:
```
docker ps
```
Busca el CONTAINER ID de rentapp, luego:

```
docker stop <CONTAINER_ID>
```

Para una limpieza completa de Docker (builds, imágenes y contenedores):

1. Primero elimina los contenedores (activos y detenidos), porque no puedes borrar una imagen si hay un contenedor que la usa.
2. Luego elimina las imágenes.
3. Finalmente, limpia el caché de build y volúmenes si quieres liberar aún más espacio.

Comando todo-en-uno para limpiar todo (contenedores, imágenes, caché y volúmenes no usados):
```
docker system prune -af --volumes
```
Esto elimina:

Todos los contenedores detenidos
Todas las imágenes no usadas por contenedores activos
Caché de build
Volúmenes no referenciados
No necesitas eliminar manualmente los builds o el caché: el comando anterior lo hace todo.

Para eliminar completamente el caché de builds, ejecuta:
```
docker builder prune -af
```
Esto borra todo el caché de compilación, incluyendo capas intermedias y builds antiguos.

Después de esto, reinicia Docker Desktop si la interfaz sigue mostrando builds antiguos.