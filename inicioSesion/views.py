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