from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    # Marcar opcionales para evitar pedir valores por defecto en migraciones
    categoria = models.CharField(max_length=24, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return self.username

class Local(models.Model):
    prop = models.CharField(max_length=33)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    direccion = models.CharField(max_length=200)
    provincia = models.CharField(max_length=200, blank=True)
    municipio = models.CharField(max_length=200, blank=True)
    sector = models.CharField(max_length=200, blank=True)
    referencia = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.direccion

class Foto(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    image_local = models.ImageField(upload_to="gallery/")
    name_foto_local = models.CharField(max_length=200, blank=True)