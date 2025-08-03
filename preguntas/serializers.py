from rest_framework import serializers
from .models import Prueba, pregunta, respuesta
from ensennanza.models import Tema
from inicioSesion.models import Usuario


class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = respuesta
        fields = ['id', 'texto']


class PreguntaSerializer(serializers.ModelSerializer):
    respuestas = serializers.SerializerMethodField()

    class Meta:
        model = pregunta
        fields = ['id', 'texto', 'respuestas']

    def get_respuestas(self, obj):
        respuestas = respuesta.objects.filter(preguntaCorespondiente=obj)
        return RespuestaSerializer(respuestas, many=True).data


class PruebaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prueba
        fields = '__all__'


class PruebaConPreguntasSerializer(serializers.ModelSerializer):
    preguntas = serializers.SerializerMethodField()

    class Meta:
        model = Prueba
        fields = ['id', 'tema', 'dificultad', 'preguntas']

    def get_preguntas(self, obj):
        preguntas = pregunta.objects.filter(temaCorespondiente=obj.tema)
        return PreguntaSerializer(preguntas, many=True).data
