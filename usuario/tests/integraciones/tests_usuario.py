import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as Usuario
from usuario.models import UserProfile
from django.test import TestCase



@pytest.mark.django_db
class TestUsuarioAPI(TestCase):
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

    def test_validacion_password_corta(self):
        client = APIClient()
        url = reverse('registro')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'short'  # contraseña muy corta
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data
        
    def test_registro_y_autenticacion_exitosa(self):
        client = APIClient()
        url_registro = reverse('registro')
        data_registro = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = client.post(url_registro, data_registro, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        url_inicio = reverse('inicio')
        data_inicio = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = client.post(url_inicio, data_inicio, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert 'usuario' in response.data
        
    def test_registro_con_datos_incompletos(self):
        client = APIClient()
        url = reverse('registro')
        data = {
            'username': 'testuser'
            # Faltan email y password
        }
        response = client.post(url, data, format='json')

        # Verificar que se devuelve un error 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verificar que se devuelva un error para el campo 'email'
        self.assertIn('email', response.data)
        
        # Verificar que se devuelva un error para el campo 'password'
        self.assertIn('password', response.data)
        
    def test_inicio_sesion_con_password_incorrecto(self):
        client = APIClient()
        user = Usuario.objects.create_user(username='testuser', password='password123')
        url = reverse('inicio')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        
    
        
