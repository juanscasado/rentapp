from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
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

    def __str__(self):
        return self.name_foto_local or f"Foto {self.id}"

# Nuevos modelos para mensajería
class Conversacion(models.Model):
    """
    Representa una conversación entre dos usuarios, opcionalmente sobre un Local.
    Se permite 1 conversación por par de usuarios POR cada Local.
    """
    participante1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversaciones_como_p1'
    )
    participante2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversaciones_como_p2'
    )
    local = models.ForeignKey(
        Local,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Local sobre el que se inició la conversación (opcional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # antes: unique_together = ['participante1', 'participante2']
        unique_together = ['participante1', 'participante2', 'local']  # clave
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversación entre {self.participante1.username} y {self.participante2.username}"

    def get_otro_participante(self, user):
        return self.participante2 if user == self.participante1 else self.participante1

    def tiene_mensajes_no_leidos(self, user):
        return self.mensajes.filter(leido=False).exclude(remitente=user).exists()

    def contar_no_leidos(self, user):
        return self.mensajes.filter(leido=False).exclude(remitente=user).count()

class Mensaje(models.Model):
    """
    Representa un mensaje dentro de una conversación.
    """
    conversacion = models.ForeignKey(
        Conversacion, 
        on_delete=models.CASCADE, 
        related_name='mensajes'
    )
    remitente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    contenido = models.TextField(max_length=1000)
    leido = models.BooleanField(default=False, db_index=True)  # Índice agregado
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Índice agregado

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversacion', '-created_at']),  # Índice compuesto
            models.Index(fields=['conversacion', 'leido']),  # Para queries de no leídos
        ]

    def __str__(self):
        return f"{self.remitente.username}: {self.contenido[:50]}"