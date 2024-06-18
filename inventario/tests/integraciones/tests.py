# Unitarias
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestInventarioAPI:
    def test_listar_productos_successfully(self):
        client = APIClient()
        url = reverse('producto-lista-crear')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK

    def test_crear_producto_successfully(self):
        client = APIClient()
        url = reverse('producto-lista-crear')
        producto_data = {
            "codigo": "001",
            "marca": "Marca1",
            "codigo_marca": "001-MARCA",
            "nombre": "Producto1",
            "precio": "100",  
            "activo": True
        }
        response = client.post(url, data=producto_data, format='json')
        
        if response.status_code != status.HTTP_201_CREATED:
            print("Response content:", response.content)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['codigo'] == producto_data['codigo']
        assert data['marca'] == producto_data['marca']
        assert data['codigo_marca'] == producto_data['codigo_marca']
        assert data['nombre'] == producto_data['nombre']
        assert data['precio'] == producto_data['precio']
        assert data['activo'] == producto_data['activo']



    def test_crear_producto_con_data_invalida(self):
        client = APIClient()
        url = reverse('producto-lista-crear')
        producto_data = {
            'codigo': '',
            'marca': 'Marca2',
            'codigo_interno': '002-INT',
            'nombre': 'Producto2',
            'precio': 2000
        }
        response = client.post(url, data=producto_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert 'codigo' in data
