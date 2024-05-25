from django.urls import path
from .views import ProductoListaCrear, ProductoDetalle

urlpatterns = [
    path('productos/', ProductoListaCrear.as_view(), name='producto-lista-crear'),
    path('productos/<int:pk>/', ProductoDetalle.as_view(), name='producto-detalle'),
]
