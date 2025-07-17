# app/urls.py
from django.urls import path
from .views import RegistroUsuarioView, InicioSesionView ,RegistroUsuarioAPIView,LoginAPIView, UsuarioListAPIView

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login', InicioSesionView.as_view(), name='login'),
    path('api/register/',RegistroUsuarioAPIView.as_view(), name='api-registro'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/usuarios/', UsuarioListAPIView.as_view(), name='usuarios-list'),
]