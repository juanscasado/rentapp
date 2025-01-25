from django.db import models
from django.contrib.auth.models import AbstractUser

from mysite import settings

class User(AbstractUser): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    categoria = models.CharField(
        max_length=24,
    # default = "propietario",
    )  
    phone = models.CharField(
        max_length=11,
    # default = "propietario",
    )  

    def __str__(self):
        return f'{self.username}'
    
  
    def get_categoria(self):
        return self.categoria
    
 
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
    image_local = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    name_foto_local = models.CharField(max_length=200)

    def __str__(self):
        return f'self.id'