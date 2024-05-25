# ecommerce/inventario/services/producto_service.py
from ..models import Producto
from ..serializers import ProductoSerializer
from rest_framework.response import Response
from rest_framework import status

def listar_productos():
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

def crear_producto(datos):
    serializer = ProductoSerializer(data=datos)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def obtener_producto(pk):
    try:
        producto = Producto.objects.get(pk=pk)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

def actualizar_producto(pk, datos):
    try:
        producto = Producto.objects.get(pk=pk)
        serializer = ProductoSerializer(producto, data=datos)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

def eliminar_producto(pk):
    try:
        producto = Producto.objects.get(pk=pk)
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)