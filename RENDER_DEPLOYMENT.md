# Guía de Deployment en Render

## Variables de entorno requeridas en Render

Configura estas variables en el dashboard de Render (Environment):

### Variables obligatorias:
```
SECRET_KEY=<genera_una_clave_segura>
DEBUG=False
ALLOWED_HOSTS=<tu-app>.onrender.com
```

Para generar una SECRET_KEY segura:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Variables de email (Gmail SMTP):
```
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_de_gmail
DEFAULT_FROM_EMAIL=tu_email@gmail.com
```

**Nota:** Usa una "App Password" de Gmail, no tu contraseña normal.

### Variables para superusuario (opcional):
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=tu_password_seguro
```

Si no las defines, se usarán los valores por defecto (admin/admin@example.com/changeme123).

### Variable automática de Render:
Render configura automáticamente:
- `RENDER_EXTERNAL_HOSTNAME` - Tu app lo detecta y añade a ALLOWED_HOSTS
- `PORT` - Gunicorn lo usa automáticamente

## Configuración del servicio en Render

1. **Build Command:**
   ```
   ./build.sh
   ```

2. **Start Command:**
   ```
   gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 3
   ```
   (Esto ya está en tu Procfile)

3. **Environment:** Python 3

4. **Branch:** main

## Pasos para deployment:

1. Asegúrate de que todos los cambios estén commiteados y pusheados:
   ```bash
   git add .
   git commit -m "fix: configuración completa para Render"
   git push origin main
   ```

2. En el dashboard de Render:
   - Ve a tu servicio web
   - Añade todas las variables de entorno listadas arriba
   - Haz clic en "Manual Deploy" → "Clear build cache & deploy"

3. Monitorea los logs para ver el progreso del build

4. Una vez completado, visita tu URL de Render

## Troubleshooting:

### Error: "No module named 'dotenv'"
- Asegúrate de que `python-dotenv` está en `requirements.txt`
- Limpia el caché y redeploy

### Error: "no such table: rentapp_local"
- Las migraciones no se ejecutaron
- Verifica que `build.sh` tiene permisos de ejecución
- Revisa los logs del build

### Error: "DisallowedHost"
- Verifica que `RENDER_EXTERNAL_HOSTNAME` está configurado correctamente
- O añade tu dominio manualmente a `ALLOWED_HOSTS` en las env vars

### Problemas de static files:
- Verifica que `collectstatic` se ejecutó en el build
- Comprueba que `STATIC_ROOT` está configurado en settings.py
- WhiteNoise debería manejar los archivos estáticos automáticamente

## Verificación post-deployment:

1. Visita tu URL principal: `https://<tu-app>.onrender.com/`
2. Accede al admin: `https://<tu-app>.onrender.com/admin/`
3. Verifica que puedes registrarte/login
4. Comprueba que los emails se envían correctamente

## Seguridad:

- **NUNCA** subas `.env` al repositorio
- Usa `DEBUG=False` en producción
- Asegúrate de usar una `SECRET_KEY` fuerte y única
- Usa App Passwords de Gmail, no tu contraseña real
- Revoca y regenera credenciales si quedan expuestas
