from django.urls import path
from .views import ProductoListaCrear, ProductoDetalle
from .views import actualizar_stock_producto

urlpatterns = [
    path('listar_productos/', ProductoListaCrear.as_view(), name='producto-lista-crear'),
    path('listar_productos_by_id/<int:pk>/', ProductoDetalle.as_view(), name='producto-detalle'),
    path('producto/<int:id_producto>/actualizar_stock/', actualizar_stock_producto, name='actualizar_stock_producto'),
]
