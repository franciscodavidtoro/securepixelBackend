from django.db import models
from inicioSesion.models import Usuario
from ensennanza.models import Tema

# Create your models here.
    
class atencion(models.Model):
    tema= models.ForeignKey(Tema, on_delete=models.CASCADE, null=True, blank=True, default=None)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, default=None)
    fecha = models.DateField(auto_now_add=True)
    vectorOjosCerados = models.JSONField(null=True, blank=True, default=None)
    vectorAnguloCabeza = models.JSONField(null=True, blank=True, default=None)
    tiempoLectura = models.FloatField(null=True, blank=True, default=None)
    
    