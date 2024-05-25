from django.contrib.auth.models import User as Usuario
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import UsuarioSerializer

@api_view(['POST'])
def inicio(request):
    usuario = get_object_or_404(Usuario, username=request.data["username"])
    if not usuario.check_password(request.data["password"]):
        return Response({"error": "Contraseña inválida"}, status=status.HTTP_400_BAD_REQUEST)
    
    (token, creado) = Token.objects.get_or_create(user=usuario)
    serializer = UsuarioSerializer(instance=usuario)

    return Response({"token": token.key, "usuario": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def registro(request):
    serializer = UsuarioSerializer(data=request.data)

    if(serializer.is_valid()):
        serializer.save()

        usuario = Usuario.objects.get(username = serializer.data['username'])
        usuario.set_password(serializer.data['password'])
        usuario.save()

        token = Token.objects.create(user=usuario)

        return Response({'token': token.key, "usuario": serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)