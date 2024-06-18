from django.urls import path
from .views import acceder, agregar_a_carro, buscar_producto, ingresar_producto, listar_producto, mi_carro, registro

urlpatterns = [
    path('acceder/', acceder, name='acceder'),
    path('agregar-a-carro/', agregar_a_carro, name='agregar-a-carro'),
    path('buscar-producto/', buscar_producto, name='buscar-producto'),
    path('ingresar-producto/', ingresar_producto, name='ingresar-producto'),
    path('listar-producto/', listar_producto, name='listar-producto'),
    path('mi-carro/', mi_carro, name='mi-carro'),
    path('registro/', registro, name='registro'),
]
