from rest_framework import serializers
from .models import Usuario

    

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'email', 'tipo_usuario']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user
    
    def update(self, instance: Usuario, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.tipo_usuario = validated_data.get('tipo_usuario', instance.tipo_usuario)
        if instance.tipo_usuario == 'administrador':
            instance.is_superuser == True
        else:
            instance.is_superuser == False

        instance.save()
        return instance
    
    def getUsuarios(self):
        usuarios = Usuario.objects.all()
        return [{'id': usuario.id, 'username': usuario.username, 'email': usuario.email, 'tipo_usuario': usuario.tipo_usuario} for usuario in usuarios]