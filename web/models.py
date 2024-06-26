from django.db import models

# Create your models here.

class producto(models.Model):
    id = models.IntegerField
    codigo_prod = models.CharField(max_length=50, blank=True, default='')
    marca_prod = models.CharField(max_length=100)
    marca_cod = models.CharField(max_length=50, blank=True, default='')
    nombre_prod = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    elaboracion = models.CharField(max_length=100, blank=True)
    activo_venta = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_prod

class user(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=40)
    
    def __str__(self):
        return self.nombre
    
class bolsa(models.Model):
    cantidad = models.IntegerField
    user_id = models.IntegerField
    producto_id = models.IntegerField

class carro(models.Model):
    
    id_producto = models.IntegerField
    cantidad = models.IntegerField
    id_user = models.IntegerField
    
class boleta(models.Model):
    respuesta = models.CharField(max_length=100)
    total_pago = models.IntegerField