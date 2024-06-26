from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PagoCarroSerializer, UsuarioSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .forms import UserForm



# views para renderizar plantillas

def acceder(request):
    return render(request, 'acceder.html')

def agregar_a_carro(request):
    return render(request, 'agregar-a-carro.html')

def buscar_producto(request):
    return render(request, 'buscar-producto.html')

def ingresar_producto(request):
    return render(request, 'ingresar-producto.html')

def listar_producto(request):
    return render(request, 'listar-producto.html')

def mi_carro(request):
    return render(request, 'mi-carro.html')

def pagar_carro(request):
    return render(request, 'pagar-carro.html')

def registro(request):
    return render(request, 'registro.html')



# Views para API

#       Registro

class RegistroView(APIView):
    def post(self, request):
        user_serializer = UsuarioSerializer(data=request.data.get('usuario'))
        if user_serializer.is_valid():
            # Crear el usuario
            user = User.objects.create_user(**user_serializer.validated_data)
            # Crear y asignar un token
            token, _ = Token.objects.get_or_create(user=user)
            response_data = {
                'token': token.key,
                'usuario': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Carrito

#       Pago
class PagarCarroView(APIView):
    def get(self, request):
        # Aquí procesamos el JSON que se recibe
        serializer = PagoCarroSerializer(data=request.query_params)  # Asumimos que se envían como parámetros de consulta
        if serializer.is_valid():
            data = serializer.validated_data
            # Aquí puedes procesar los datos como necesites
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

