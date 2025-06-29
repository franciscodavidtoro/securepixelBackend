# app/urls.py
from django.urls import path
from .views import RegistroUsuarioView, InicioSesionView

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login', InicioSesionView.as_view(), name='login')
]