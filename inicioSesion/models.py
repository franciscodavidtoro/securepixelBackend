from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.exceptions import ValidationError
from ensennanza.models import Curso

class UsuarioManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('tipo_usuario', 'administrador')
        return super().create_superuser(username, email, password, **extra_fields)



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
    curso=models.ForeignKey(Curso,null=True,default=None,blank=True,
        on_delete=models.SET_NULL, related_name='alumnos' )

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"
    

        
            

    