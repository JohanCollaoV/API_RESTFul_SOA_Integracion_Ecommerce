from rest_framework import serializers
from django.contrib.auth.models import User as Usuario
from django.core.exceptions import ValidationError

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return value