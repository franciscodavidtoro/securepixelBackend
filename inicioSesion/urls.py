# app/urls.py
from django.urls import path
from .views import (
    RegistroUsuarioAPIView,
    LoginAPIView,
    UsuarioListAPIView,
    UsuariosUpdateAPIView,
    UsuarioCambContrasennaAPIView,
    LogoutAPIView,
    UsuarioActualAPIView
)

urlpatterns = [
    path('register', RegistroUsuarioAPIView.as_view(), name='api-registro'),
    path('login', LoginAPIView.as_view(), name='api-login'),
    path('usuarios', UsuarioListAPIView.as_view(), name='usuarios-list'),
    path('update', UsuariosUpdateAPIView.as_view(), name='usuarios-update'),
    path('cambiar-contrasena', UsuarioCambContrasennaAPIView.as_view(), name='usuarios-cambiar-contrasena'),
    path('logout', LogoutAPIView.as_view(), name='api-logout'),
    path('yo', UsuarioActualAPIView.as_view(), name='usuario-actual')
]