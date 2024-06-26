from django.db import models
from inventario.models import Producto
from django.contrib.auth.models import User as Usuario

class Carro(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    
    def __str__(self):
        return f'{self.id_usuario.username} - {self.id_producto.nombre}'