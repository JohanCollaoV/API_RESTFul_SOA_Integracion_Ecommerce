from django.contrib.auth.models import User as Usuario
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UsuarioSerializer
from rest_framework.exceptions import ValidationError
from .models import UserProfile

from django.contrib.auth.models import User as Usuario
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UsuarioSerializer
from rest_framework.exceptions import ValidationError
from .models import UserProfile

@api_view(['POST'])
def registro(request):
    data = request.data

    # Verificar el tipo de dato de la contraseña
    if isinstance(data.get("password"), int):
        password_type = 'integer'
    elif isinstance(data.get("password"), str):
        password_type = 'string'
    else:
        return Response({"error": "El tipo de contraseña no es válido"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UsuarioSerializer(data=data)

    if serializer.is_valid():
        # Crear el usuario sin guardar aún
        usuario = Usuario(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )

        # Establecer la contraseña encriptada
        usuario.set_password(serializer.validated_data['password'])
        usuario.save()

        # Guardar el tipo de contraseña en el perfil del usuario
        user_profile, created = UserProfile.objects.get_or_create(user=usuario)
        user_profile.password_type = password_type
        user_profile.save()

        token = Token.objects.create(user=usuario)

        # Eliminar el campo de contraseña de la respuesta
        usuario_data = serializer.data
        usuario_data.pop('password', None)

        return Response({'token': token.key, "usuario": usuario_data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def inicio(request):
    try:
        usuario = get_object_or_404(Usuario, username=request.data.get("username"))

        # Verificar el tipo de dato de la contraseña ingresada
        input_password = request.data.get("password")
        if isinstance(input_password, int):
            input_password_type = 'integer'
        elif isinstance(input_password, str):
            input_password_type = 'string'
        else:
            return Response({"error": "El tipo de contraseña no es válido"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar que el tipo de contraseña coincida
        user_profile = get_object_or_404(UserProfile, user=usuario)
        if user_profile.password_type != input_password_type:
            raise ValidationError({"error": "El tipo de contraseña no es válido"})

        # Verificar la contraseña
        if not usuario.check_password(str(input_password)):
            raise ValidationError({"error": "Contraseña inválida"})

        token, created = Token.objects.get_or_create(user=usuario)
        serializer = UsuarioSerializer(instance=usuario)

        # Eliminar el campo de contraseña de la respuesta
        usuario_data = serializer.data
        usuario_data.pop('password', None)

        return Response({"token": token.key, "usuario": usuario_data}, status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST) 

    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no existe"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)