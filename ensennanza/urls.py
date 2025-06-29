# app/urls.py
from django.urls import path
from .views import TemaListView,TemaDetailView

urlpatterns = [
    path('', TemaListView.as_view(), name='tema-list'),
    path('<int:pk>/', TemaDetailView.as_view(), name='tema-detail'),
]