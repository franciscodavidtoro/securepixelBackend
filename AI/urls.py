from django.urls import path
from .views import AtencionAPIView, ProcesarImgEmocionesAPIView

urlpatterns = [
    path('atencion', AtencionAPIView.as_view(), name='api-atencion'),
    path('emociones/<int:pk>', ProcesarImgEmocionesAPIView.as_view(), name='api-emociones'),
]
