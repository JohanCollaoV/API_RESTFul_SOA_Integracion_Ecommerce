"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from usuario import views as ViewUsuario
from carro import views as ViewCarro
from pago import views as ViewPago

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('inventario.urls')),
    path('', include('web.urls')),
    path('api/registro/', ViewUsuario.registro, name='registro'),
    path('api/acceder/', ViewUsuario.inicio, name='inicio'),
    path('api/carrito-agregar/', ViewCarro.agregarProducto, name='agregar_producto'),
    path('api/carrito-mostrar/', ViewCarro.mostrarProducto, name='mostrar_carrito'),
    path('api/carrito-eliminar/<int:producto_id>/', ViewCarro.eliminarProducto, name='eliminar_producto'),
    path('api/carrito-actualizar/<int:producto_id>/', ViewCarro.actualizarCantidadProducto, name='actualizar_producto'),
    path('api/carrito-vaciar/', ViewCarro.vaciarCarro, name='vaciar_carrito'),
    path('api/pagar/', ViewPago.pagarCarro, name='pagar_carrito'),
]
