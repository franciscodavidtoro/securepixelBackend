from django.shortcuts import render

# app/views.py

from .models import Usuario



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UsuarioSerializer
from rest_framework.permissions import IsAuthenticated


class RegistroUsuarioAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        
        if serializer.is_valid():
            if not Usuario.objects.exists():
                serializer.validated_data['is_staff'] = True
                serializer.validated_data['is_superuser'] = True
                serializer.validated_data['tipo_usuario'] = 'administrador'
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
class UsuarioListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        usuario=request.user # type: Usuario
        
        if usuario.tipo_usuario =="Administrador" or usuario.is_superuser:
            
            usuarios = Usuario.objects.all()
            serializer = UsuarioSerializer(usuarios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif usuario.tipo_usuario =="Profesor":
            serializer = UsuarioSerializer()
            usuarios = serializer.getUsuariosProfesor(usuario)
            return Response(usuarios, status=status.HTTP_200_OK)
        return Response({'error': 'No tiene permisos'}, status=status.HTTP_401_UNAUTHORIZED)
    
class UsuariosUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        usuario_autenticado = request.user  # type: Usuario

        try:
            usuario_objetivo = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Permitir si es el mismo usuario o si es admin y superusuario
        if usuario_autenticado.id == id or usuario_autenticado.is_superuser:
            serializer = UsuarioSerializer(usuario_objetivo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # Aquí se usa tu método update() personalizado
                return Response({'message': 'Usuario actualizado correctamente'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'No tienes permiso para modificar este usuario.'}, status=status.HTTP_403_FORBIDDEN)

        
        
        
class UsuarioCambContrasennaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        usuario_autenticado = request.user  # type: Usuario
        nueva_contrasena = request.data.get('nueva_contrasena')
        id_usuario_objetivo = pk

        if not nueva_contrasena:
            return Response({'detail': 'Debe proporcionar una nueva contraseña.'}, status=status.HTTP_400_BAD_REQUEST)

        # Si no se especifica ID, se asume que el usuario quiere cambiar su propia contraseña
        if not id_usuario_objetivo:
            id_usuario_objetivo = usuario_autenticado.pk

        # Verificamos si es el mismo usuario que quiere cambiar su propia contraseña
        if usuario_autenticado.pk == int(id_usuario_objetivo):
            usuario_autenticado.set_password(nueva_contrasena)
            usuario_autenticado.save()
            return Response({'message': 'Contraseña actualizada correctamente.'})

        # Si no es el mismo usuario pero es Administrador, puede cambiar contraseñas de otros
        if usuario_autenticado.tipo_usuario == "Administrador" or usuario_autenticado.is_superuser:
            try:
                usuario_objetivo = Usuario.objects.get(pk=id_usuario_objetivo)
            except Usuario.DoesNotExist:
                return Response({'detail': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            usuario_objetivo.set_password(nueva_contrasena)
            usuario_objetivo.save()
            return Response({'message': 'Contraseña de otro usuario actualizada correctamente.'})

        # Si no es el mismo usuario y no es administrador, no tiene permiso
        return Response({'detail': 'No tienes permiso para modificar esta contraseña.'},
                        status=status.HTTP_403_FORBIDDEN)
        
     

        
    

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Elimina el token
        return Response({'message': 'Sesión cerrada'}, status=status.HTTP_200_OK)
    
    
    
class UsuarioActualAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)