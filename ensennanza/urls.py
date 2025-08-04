from django.urls import path
from .views import (
    CursoCrearListarAPI, CursoLeerActualizarEliminarAPI,
    TemaCrearListarAPI, TemaLeerActualizarEliminarAPI,
    TemaSiguiente
)

urlpatterns = [
    # Cursos
    path('cursos/', CursoCrearListarAPI.as_view(), name='curso-listar-crear'),
    path('cursos/<int:pk>/', CursoLeerActualizarEliminarAPI.as_view(), name='curso-leer-actualizar-eliminar'),

    # Temas
    path('temas/', TemaCrearListarAPI.as_view(), name='tema-listar-crear'),
    path('temas/<int:pk>/', TemaLeerActualizarEliminarAPI.as_view(), name='tema-leer-actualizar-eliminar'),

    # Tema siguiente
    path('temas/siguiente/', TemaSiguiente.as_view(), name='tema-siguiente'),
]
