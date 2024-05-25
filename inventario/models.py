from django.db import models

# Create your models here.

class Producto(models.Model):
    codigo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    codigo_marca = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=12, decimal_places=0) 
    creado_en = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)  # Nuevo campo para indicar si el producto está activo o no


    def __str__(self):
        return self.nombre