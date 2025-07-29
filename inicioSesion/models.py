from django.contrib.auth.models import AbstractUser
from django.db import models


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

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"