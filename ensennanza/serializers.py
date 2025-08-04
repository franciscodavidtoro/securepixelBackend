from rest_framework import serializers
from .models import Curso,Tema

class CursoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'
        
class TemaSerializers(serializers.ModelSerializer):
    contenido_formateado = serializers.SerializerMethodField()
    class Meta:
        model = Tema
        fields = ['id', 'titulo', 'contenido', 'curso', 'orden', 'contenido_formateado']

    def get_contenido_formateado(self, obj):
        return obj.formatted_markdown()
        
    