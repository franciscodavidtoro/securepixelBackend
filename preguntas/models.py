from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
# Create your models here.
from ensennanza.models import Tema
from inicioSesion.models import Usuario
from django.core.validators import MinValueValidator, MaxValueValidator


class subirImg(models.Model):
    
    imagen = models.ImageField(upload_to='imagenesSubidas/')
    
    def __str__(self):
        return str(self.imagen.name)
    
class pregunta(models.Model):
    temaCorespondiente = models.ForeignKey(Tema, on_delete=models.CASCADE, null=True, blank=True, default=None)
    ia = models.BooleanField(default=False)
    IAPrompt=models.TextField( null=True, blank=True, default="")
    texto = MarkdownxField()
    
    
        
    def __str__(self):
        return self.temaCorespondiente.__str__()
    
class respuesta(models.Model):
    preguntaCorespondiente=models.ForeignKey(pregunta, on_delete=models.CASCADE)
    texto=MarkdownxField()
    corecta= models.BooleanField(default=False)
    ia=models.BooleanField(default=False)
    def __str__(self):
        return markdownify(self.texto)


class Prueba(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, null=True, blank=True)
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    realizada = models.BooleanField(default=False)
    calificacion = models.FloatField(default=0.0)
    dificultad=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    repetible =models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)