from django.db import models
from inventario.models import Producto

class Carro(models.Model):
    pass

"""
    Cuando se hacer POST
    Se genera un carro con un id
    a CarroProducto se le asigna el id del Carro
"""