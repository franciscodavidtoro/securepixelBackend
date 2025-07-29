

# Create your models here.
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from inicioSesion.models import Curso

class Tema(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = MarkdownxField()
    curso=models.ForeignKey(Curso,on_delete=models.PROTECT,null=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        unique_together = ('curso', 'orden')

    def __str__(self):
        return self.titulo
    
    def formatted_markdown(self):
        return markdownify(self.contenido)

    
    