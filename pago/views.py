from django.db import transaction
from django.db.models import F
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from carro.models import Carro
from inventario.models import Producto
from pago.models import Pago

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def pagarCarro(request):
    if not request.user.id:
        return Response({'error': 'Usuario sin carro', 'estado_pago': 'Pago rechazado'}, status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        carros = Carro.objects.select_for_update().filter(id_usuario=request.user.id)
        if not carros.exists():
            return Response({'error': 'El carro está vacío'}, status=status.HTTP_400_BAD_REQUEST)

        total = 0
        detalles = []

        for carro in carros:
            producto = carro.id_producto
            if producto.stock < carro.cantidad:
                return Response({'error': f'No hay suficiente stock para {producto.nombre}'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            subtotal = producto.precio * carro.cantidad
            total += subtotal
            producto.stock = F('stock') - carro.cantidad
            producto.save()
            detalles.append({'producto': producto.nombre, 'cantidad': carro.cantidad, 'precio': subtotal})
        
        if total > 0:
            Pago.objects.create(id_usuario=request.user, total=total)
            carros.delete()

        return Response({'respuesta': 'pago_realizado', 'total_pagado': total, 'detalle_pago': detalles}, status=status.HTTP_201_CREATED)

