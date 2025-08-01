from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.apps import apps



class Curso(models.Model):
    profesor=models.ForeignKey('inicioSesion.Usuario',on_delete=models.PROTECT,limit_choices_to={'tipo_usuario': 'profesor'},related_name='cursos_dictados')
    nombreCurso=models.CharField(max_length=70)
    dificultadMinima = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    dificultadMaxima = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    def clean(self):
        super().clean()
        if self.dificultadMinima > self.dificultadMaxima:
            raise ValidationError("La dificultad mínima no puede ser mayor que la máxima.")
    def __str__(self):
        return self.nombreCurso

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


    