import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

## PRUEBAS UNITARIAS Y DE INTEGRACION

@pytest.mark.django_db
class TestUsuarioAPI:
    def test_creacion_usuario_exitosa(self):
        client = APIClient()
        url = reverse('registro')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'token' in response.data
        assert 'usuario' in response.data


    def test_validacion_email_invalido(self):
        client = APIClient()
        url = reverse('registro')
        data = {
            'username': 'testuser',
            'email': 'invalidemail',  # email inválido
            'password': 'password123'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    