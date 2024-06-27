import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from inventario.models import Producto
from carro.models import Carro
from pago.models import Pago

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def setup_user_and_token():
    user = User.objects.create_user(username='testuser', password='testpassword')
    token = Token.objects.create(user=user)
    return user, token

@pytest.fixture
def setup_product_and_cart(setup_user_and_token):
    user, token = setup_user_and_token
    producto = Producto.objects.create(nombre='Producto de prueba', precio=10, stock=5)
    carro = Carro.objects.create(id_usuario=user, id_producto=producto, cantidad=2)
    return user, token, producto, carro

## PRUEBAS UNITARIAS


@pytest.mark.django_db
def test_pagar_carro_vacio(api_client, setup_user_and_token):
    user, token = setup_user_and_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('pagar_carrito')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'El carro está vacío'



@pytest.mark.django_db
def test_pagar_carro_sin_autenticacion(api_client, setup_product_and_cart):
    user, token, producto, carro = setup_product_and_cart
    url = reverse('pagar_carrito')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
@pytest.mark.django_db
def test_pagar_carro_exitoso(api_client, setup_product_and_cart):
    user, token, producto, carro = setup_product_and_cart
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('pagar_carrito')
    response = api_client.post(url)

    assert response.status_code == status.HTTP_201_CREATED
    assert 'respuesta' in response.data
    assert 'total_pagado' in response.data
    assert 'detalle_pago' in response.data

    # Verificar que se haya creado el registro de pago en la base de datos
    assert Pago.objects.filter(id_usuario=user).exists()
    
@pytest.mark.django_db
def test_pagar_carro_con_stock_insuficiente(api_client, setup_product_and_cart):
    user, token, producto, carro = setup_product_and_cart
    producto.stock = 1  # Establecer stock insuficiente para el pago
    producto.save()
    
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('pagar_carrito')
    response = api_client.post(url)
    
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert 'No hay suficiente stock' in response.data['error']

## PRUEBAS DE INTEGRACION


@pytest.mark.django_db
def test_pagar_carro_sin_autenticacion_integracion(api_client):
    url = reverse('pagar_carrito')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_pagar_carro_stock_suficiente_integracion(api_client, setup_user_and_token):
    user, token = setup_user_and_token
    producto = Producto.objects.create(nombre='Producto suficiente', precio=5, stock=20)
    Carro.objects.create(id_usuario=user, id_producto=producto, cantidad=10)
    
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('pagar_carrito')
    response = api_client.post(url)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Producto.objects.get(pk=producto.pk).stock == 10

@pytest.mark.django_db
def test_pagar_carro_multiple_productos(api_client, setup_user_and_token):
    user, token = setup_user_and_token
    producto1 = Producto.objects.create(nombre='Producto 1', precio=20, stock=10)
    producto2 = Producto.objects.create(nombre='Producto 2', precio=15, stock=5)
    Carro.objects.create(id_usuario=user, id_producto=producto1, cantidad=1)
    Carro.objects.create(id_usuario=user, id_producto=producto2, cantidad=3)
    
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('pagar_carrito')
    response = api_client.post(url)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Pago.objects.filter(id_usuario=user).exists()
    assert Producto.objects.get(pk=producto1.pk).stock == 9
    assert Producto.objects.get(pk=producto2.pk).stock == 2
    
@pytest.mark.django_db
def test_pagar_carro_actualizacion_stock(api_client, setup_product_and_cart):
    user, token, producto, carro = setup_product_and_cart
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    url = reverse('pagar_carrito')
    initial_stock = producto.stock
    
    response = api_client.post(url)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Producto.objects.get(pk=producto.pk).stock == initial_stock - carro.cantidad