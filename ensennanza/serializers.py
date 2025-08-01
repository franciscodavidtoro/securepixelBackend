from rest_framework import serializers
from .models import Curso,Tema

class CursoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'
        
class TemaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = '__all__'
        
    