# app/urls.py
from django.urls import path
from .views import (
    AdminDasboardEstadisticasAPIView,
    ReporteEstadisticasGeneralesAPIView,
    ReporteAtencionEstudiantesAPIView,
    ReporteEmocionesEstudiantesAPIView,
    ProfesorDasboardEstadisticasAPIView
    )

urlpatterns = [
    path('admin-dashboard', AdminDasboardEstadisticasAPIView.as_view(), name='admin-dashboard-estadisticas'),
    path('reporte-estadisticas-generales', ReporteEstadisticasGeneralesAPIView.as_view(), name='reporte-estadisticas-generales'),
    path('reporte-atencion-estudiantes', ReporteAtencionEstudiantesAPIView.as_view(), name='reporte-atencion-estudiantes'),
    path('reporte-emociones-estudiantes', ReporteEmocionesEstudiantesAPIView.as_view(), name='reporte-emociones-estudiantes'),
    path('profesor-dashboard', ProfesorDasboardEstadisticasAPIView.as_view(), name='profesor-dashboard-estadisticas')
]   