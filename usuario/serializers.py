from rest_framework import serializers
from django.contrib.auth.models import User as Usuario
from django.core.exceptions import ValidationError

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password',]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Introduzca una dirección de correo electrónico válida.")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return value