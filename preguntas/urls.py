from django.urls import path
from .views import CrearPruebaAPIView, ObtenerPreguntasDePruebaAPIView, RealizarPruebaAPIView,ListarPruebasAPIView, PruebaDetalleAPIView



urlpatterns = [
    path('crear-prueba/', CrearPruebaAPIView.as_view(), name='crear-prueba'),
    path('prueba/<int:pk>/', ObtenerPreguntasDePruebaAPIView.as_view(), name='ver-prueba'),
    path('prueba/<int:pk>/responder/', RealizarPruebaAPIView.as_view(), name='responder-prueba'),
    path('listar-pruebas/', ListarPruebasAPIView.as_view(), name='listar-pruebas'),
    path('detalle-prueba/<int:pk>/', PruebaDetalleAPIView.as_view(), name='detalle-prueba')
]
