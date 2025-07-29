from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Curso(models.Model):
    profesor=models.ForeignKey('Usuario',on_delete=models.PROTECT,limit_choices_to={'tipo_usuario': 'profesor'},related_name='cursos_dictados')
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

class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ('alumno', 'Alumno'),
        ('profesor', 'Profesor'),
        ('administrador', 'Administrador'),
    ]
    
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPOS_USUARIO,
        default='alumno',
    )
    Curso=models.ForeignKey(Curso,null=True,default=None,blank=True,
        on_delete=models.SET_NULL, related_name='alumnos' )

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"
    
    def clean(self):
        super().clean()
        
        # Si NO es alumno, Curso debe ser null
        if self.tipo_usuario != 'alumno' and self.Curso is not None:
            raise ValidationError({'Curso': 'Solo los alumnos pueden tener curso asignado.'})

    