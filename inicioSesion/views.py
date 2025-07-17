from django.shortcuts import render

# app/views.py
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Usuario
from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UsuarioSerializer
from rest_framework.permissions import IsAuthenticated




class RegistroUsuarioView(CreateView):
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = 'registro.html'
    success_url = reverse_lazy('login')
    
    
class InicioSesionView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('login_success')  # Ruta dummy, sobreescribiremos post()

    def form_valid(self, form):
        """Si el formulario es válido, autenticamos y devolvemos respuesta directa."""
        from django.contrib.auth import login
        login(self.request, form.get_user())
        return HttpResponse("Inicio de sesión correcto", status=200)

    def form_invalid(self, form):
        """Si el formulario es inválido, mostrar el formulario otra vez."""
        return render(self.request, self.template_name, {'form': form})
    



class RegistroUsuarioAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
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
        serializer = UsuarioSerializer()
        usuarios = serializer.getUsuarios()
        return Response(usuarios, status=status.HTTP_200_OK)
    
