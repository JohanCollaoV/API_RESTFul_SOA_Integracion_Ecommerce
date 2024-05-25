from rest_framework import serializers
from django.contrib.auth.models import User as Usuario
from .models import Carro

class CarroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carro
        fields = '__all__'