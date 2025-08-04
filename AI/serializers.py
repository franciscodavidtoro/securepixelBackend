from rest_framework import serializers
from .models import atencion,emociones

class AtencionSerializer(serializers.ModelSerializer):
    class Meta:
        model = atencion
        fields = '__all__'
        read_only_fields = ['fecha']

class EmocionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = emociones
        fields = '__all__'
        read_only_fields = ['prueba', 'emociones','emocionPredominante', 'numImgProsesadas']
  
        
    
    
    