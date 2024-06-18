from rest_framework import serializers

# Registro
from rest_framework import serializers

class UsuarioSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # El ID se genera automáticamente al guardar el usuario
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class RegistroSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, read_only=True)
    usuario = UsuarioSerializer()

# Carrito


# Pago
class DetallePagoSerializer(serializers.Serializer):
    producto = serializers.CharField(max_length=200)
    cantidad = serializers.IntegerField()
    precio = serializers.FloatField()

class PagoCarroSerializer(serializers.Serializer):
    respuesta = serializers.CharField(max_length=100)
    total_pagado = serializers.FloatField()
    detalle_pago = DetallePagoSerializer(many=True)
