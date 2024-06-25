from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class ProductoListaCrear(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def actualizar_stock_producto(request, id_producto):
    try:
        producto = Producto.objects.get(id=id_producto)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    nuevo_stock = request.data.get('stock')
    if nuevo_stock is not None and nuevo_stock >= 0:
        producto.stock = nuevo_stock
        producto.save()
        return Response({'message': 'Stock actualizado exitosamente'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Cantidad de stock inválida'}, status=status.HTTP_400_BAD_REQUEST)

