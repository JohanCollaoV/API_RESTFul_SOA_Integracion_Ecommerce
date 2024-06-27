import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from inventario.models import Producto
from carro.models import Carro
from decimal import Decimal 

## PRUEBAS UNITARIAS Y DE INTEGRACION

@pytest.mark.django_db
class TestCarroAPI:
    
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.producto = Producto.objects.create(nombre='Producto Test', precio=100, stock=10)


    def test_eliminar_producto_carro(self):
        carro = Carro.objects.create(id_usuario=self.user, id_producto=self.producto, cantidad=2)
        url = reverse('eliminar_producto', args=[carro.id_producto.id])
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'Producto eliminado del carro'

    def test_actualizar_cantidad_producto_carro(self):
        carro = Carro.objects.create(id_usuario=self.user, id_producto=self.producto, cantidad=1)
        url = reverse('actualizar_producto', args=[carro.id_producto.id])
        data = {
            'cantidad': 3
        }
        response = self.client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'Cantidad actualizada'

    def test_vaciar_carro(self):
        Carro.objects.create(id_usuario=self.user, id_producto=self.producto, cantidad=2)
        url = reverse('vaciar_carrito')
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'Carro vaciado'


    def test_pagar_carro_sin_productos(self):
        url = reverse('pagar_carrito')
        response = self.client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert response.data['error'] == 'El carro está vacío'

    def test_eliminar_producto_no_existente(self):
        url = reverse('eliminar_producto', args=[999])  # 999 es un ID que sabemos que no existe
        response = self.client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data
        assert response.data['error'] == 'Producto no encontrado en el carro'
    
    def test_agregar_producto_carro_sin_autenticacion(self):
        url = reverse('agregar_producto')
        data = {
            'id_producto': self.producto.id,
            'cantidad': 2
        }
        client = APIClient()  # Crear un nuevo cliente sin autenticación
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data

        # Verificar que el mensaje de error contenga la frase clave esperada
        error_detail = response.data['detail']
        assert isinstance(error_detail, str)  # Asegurarse de que el error sea una cadena
        assert 'credenciales de autenticación no se proveyeron' in error_detail.lower()
        
    def test_mostrar_producto_carro_sin_autenticacion(self):
        url = reverse('mostrar_carrito')
        client = APIClient()  # Crear un nuevo cliente sin autenticación
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data

        # Verificar que el mensaje de error contenga la frase clave esperada
        error_detail = response.data['detail']
        assert isinstance(error_detail, str)  # Asegurarse de que el error sea una cadena
        assert 'credenciales de autenticación no se proveyeron' in error_detail.lower()

        
    from decimal import Decimal

    def test_pagar_carro_con_productos_suficientes(self):
        # Crear un carro con productos suficientes
        Carro.objects.create(id_usuario=self.user, id_producto=self.producto, cantidad=1)

        # Simular el pago del carro
        url = reverse('pagar_carrito')
        response = self.client.post(url)

        # Verificar que la respuesta sea exitosa y verificar la estructura de datos devuelta
        assert response.status_code == status.HTTP_201_CREATED
        assert 'detalle_pago' in response.data
        assert 'respuesta' in response.data
        assert 'total_pagado' in response.data
        assert response.data['respuesta'] == 'pago_realizado'
        assert response.data['total_pagado'] == Decimal('100')  # Convertir '100' a Decimal
        assert len(response.data['detalle_pago']) == 1  # Asegúrate de que haya un solo elemento en 'detalle_pago'

        detalle_pago = response.data['detalle_pago'][0]
        assert detalle_pago['cantidad'] == 1
        assert detalle_pago['precio'] == Decimal('100')  # Convertir '100' a Decimal


        