from rest_framework import serializers
from .models import Usuario


    

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password','first_name','last_name', 'email', 'tipo_usuario', 'curso', 'is_superuser']
        read_only_fields = ['id', 'is_superuser']
    
    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user
    
    def update(self, instance: Usuario, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
    
        
        if instance.tipo_usuario == 'administrador':
            instance.is_superuser = True
            instance.is_staff = True
        else:
            instance.is_superuser == False

        instance.save()
        return instance
    
    
    
    def getUsuariosProfesor(self, instance: Usuario):
        # Obtener usuarios tipo 'alumno' cuyo curso tenga como profesor al 'instance'
        alumnos = Usuario.objects.filter(
            tipo_usuario='alumno',
            curso__profesor=instance,
        )

        return [
            {
                'id': alumno.id,
                'username': alumno.username,
                'email': alumno.email,
                'tipo_usuario': alumno.tipo_usuario
            }
            for alumno in alumnos
        ]
    
    def update_admin_password(self, instance: Usuario, new_password: str):
        if instance.tipo_usuario != 'administrador':
            raise serializers.ValidationError("El usuario no es un administrador.")
        instance.set_password(new_password)
        instance.save()
        return instance
    
    def update_user_password(self, instance: Usuario, new_password: str):
        instance.set_password(new_password)
        instance.save()
        return instance

