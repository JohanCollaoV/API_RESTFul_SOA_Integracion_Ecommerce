from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer

class ProductoListaCrear(generics.ListCreateAPIView):
    serializer_class = ProductoSerializer

    def get_queryset(self):
        return Producto.objects.filter(activo=True)

class ProductoDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


