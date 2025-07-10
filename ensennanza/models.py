

# Create your models here.
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from inicioSesion.models import Usuario

class Tema(models.Model):
    titulo = models.CharField(max_length=200)
    dificultadMinima = models.IntegerField()
    dificultadMaxima = models.IntegerField()
    contenido = MarkdownxField()


    def __str__(self):
        return self.titulo
    
    def formatted_markdown(self):
        return markdownify(self.contenido)

    
    