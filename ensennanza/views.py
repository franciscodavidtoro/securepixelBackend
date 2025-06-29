from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Tema

class TemaListView(ListView):
    model = Tema
    template_name = 'Tema_list.html'  # Opcional si sigue convención
    context_object_name = 'Temas'
    ordering = ['-titulo']

class TemaDetailView(DetailView):
    model = Tema
    template_name = 'Tema_detail.html'
    context_object_name = 'Tema'