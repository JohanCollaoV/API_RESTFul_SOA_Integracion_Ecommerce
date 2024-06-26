import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


## PRUEBAS UNITARIAS

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
            "activo": True,
            "stock": 50  # Añadir el campo 'stock'
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
        assert data['stock'] == producto_data['stock']  # Verificar el campo 'stock'

    def test_crear_producto_con_data_invalida(self):
        client = APIClient()
        url = reverse('producto-lista-crear')
        producto_data = {
            'codigo': '',
            'marca': 'Marca2',
            'codigo_interno': '002-INT',
            'nombre': 'Producto2',
            'precio': 2000,
            'stock': 30  # Añadir el campo 'stock'
        }
        response = client.post(url, data=producto_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert 'codigo' in data

    def test_actualizar_producto_successfully(self):
        # Crear un producto inicialmente
        client = APIClient()
        url = reverse('producto-lista-crear')
        producto_data = {
            "codigo": "004",
            "marca": "Marca4",
            "codigo_marca": "004-MARCA",
            "nombre": "Producto4",
            "precio": "400",
            "activo": True,
            "stock": 100  # Añadir el campo 'stock'
        }
        response = client.post(url, data=producto_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        # Actualizar el producto creado
        producto_id = response.json()['id']
        url_detalle = reverse('producto-detalle', args=[producto_id])
        datos_actualizados = {
            "codigo": "004",
            "marca": "Marca4-Actualizada",
            "codigo_marca": "004-MARCA",
            "nombre": "Producto4-Actualizado",
            "precio": "450",
            "activo": False,
            "stock": 80  # Añadir el campo 'stock'
        }
        response = client.put(url_detalle, data=datos_actualizados, format='json')
        assert response.status_code == status.HTTP_200_OK

        # Verificar que los datos actualizados están correctos
        data = response.json()
        assert data['marca'] == datos_actualizados['marca']
        assert data['nombre'] == datos_actualizados['nombre']
        assert data['precio'] == datos_actualizados['precio']
        assert data['activo'] == datos_actualizados['activo']
        assert data['stock'] == datos_actualizados['stock']  # Verificar el campo 'stock'


##PRUEBAS DE INTEGRACION
    def test_crear_y_listar_productos(self):
        client = APIClient()
        url = reverse('producto-lista-crear')
        producto_data = {
            "codigo": "005",
            "marca": "Marca5",
            "codigo_marca": "005-MARCA",
            "nombre": "Producto5",
            "precio": "500",
            "activo": True,
            "stock": 60
        }
        # Crear un producto
        response = client.post(url, data=producto_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        # Listar productos y verificar que el producto creado está presente
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert any(producto['codigo'] == producto_data['codigo'] for producto in data)

    def test_actualizar_y_obtener_detalle_producto(self):
        client = APIClient()
        url = reverse('producto-lista-crear')
        producto_data = {
            "codigo": "006",
            "marca": "Marca6",
            "codigo_marca": "006-MARCA",
            "nombre": "Producto6",
            "precio": "600",
            "activo": True,
            "stock": 70
        }
        # Crear un producto
        response = client.post(url, data=producto_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        producto_id = response.json()['id']

        # Actualizar el producto
        url_detalle = reverse('producto-detalle', args=[producto_id])
        datos_actualizados = {
            "codigo": "006",
            "marca": "Marca6-Actualizada",
            "codigo_marca": "006-MARCA",
            "nombre": "Producto6-Actualizado",
            "precio": "650",
            "activo": False,
            "stock": 75
        }
        response = client.put(url_detalle, data=datos_actualizados, format='json')
        assert response.status_code == status.HTTP_200_OK

        # Obtener el detalle del producto y verificar los datos actualizados
        response = client.get(url_detalle)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['marca'] == datos_actualizados['marca']
        assert data['nombre'] == datos_actualizados['nombre']
        assert data['precio'] == datos_actualizados['precio']
        assert data['activo'] == datos_actualizados['activo']
        assert data['stock'] == datos_actualizados['stock']

    def test_eliminar_y_verificar_producto(self):
        client = APIClient()
        url = reverse('producto-lista-crear')
        producto_data = {
            "codigo": "007",
            "marca": "Marca7",
            "codigo_marca": "007-MARCA",
            "nombre": "Producto7",
            "precio": "700",
            "activo": True,
            "stock": 80
        }
        # Crear un producto
        response = client.post(url, data=producto_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        producto_id = response.json()['id']

        # Eliminar el producto
        url_detalle = reverse('producto-detalle', args=[producto_id])
        response = client.delete(url_detalle)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar que el producto ya no existe
        response = client.get(url_detalle)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_crear_productos_en_masa_y_verificar_listado(self):
        client = APIClient()
        url = reverse('producto-lista-crear')
        productos_data = [
            {
                "codigo": "008",
                "marca": "Marca8",
                "codigo_marca": "008-MARCA",
                "nombre": "Producto8",
                "precio": "800",
                "activo": True,
                "stock": 90
            },
            {
                "codigo": "009",
                "marca": "Marca9",
                "codigo_marca": "009-MARCA",
                "nombre": "Producto9",
                "precio": "900",
                "activo": True,
                "stock": 100
            }
        ]
        # Crear múltiples productos
        for producto_data in productos_data:
            response = client.post(url, data=producto_data, format='json')
            assert response.status_code == status.HTTP_201_CREATED

        # Listar productos y verificar que todos los productos creados están presentes
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for producto_data in productos_data:
            assert any(producto['codigo'] == producto_data['codigo'] for producto in data)