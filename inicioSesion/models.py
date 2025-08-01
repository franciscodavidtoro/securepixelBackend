from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from ensennanza.models import Curso




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

    