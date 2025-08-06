from rest_framework import serializers
from .models import Prueba, pregunta, respuesta
from ensennanza.models import Tema
from inicioSesion.models import Usuario
from AI.GeneradorRespuestas import completar_respuestas_ia_con_contexto


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
        resultado = []

        for p in preguntas:
            respuestas_existentes = respuesta.objects.filter(preguntaCorespondiente=p, ia=False)
            respuestas_ia = respuesta.objects.filter(preguntaCorespondiente=p, ia=True)

            # Serializamos respuestas existentes
            respuestas_serializadas = [
                {
                    "id": r.id,
                    "texto": r.texto,
                    "corecta": r.corecta,
                    "ia": False
                }
                for r in respuestas_existentes
            ]

            if p.ia and respuestas_ia.exists():
                instrucciones = [
                    {"id": r.id, "texto": r.texto, "corecta": r.corecta}
                    for r in respuestas_ia
                ]
                contexto = [
                    {"texto": r.texto, "corecta": r.corecta}
                    for r in respuestas_existentes
                ]

                dificultad = getattr(p, "dificultad", getattr(obj, "dificultad", 5))

                generadas = completar_respuestas_ia_con_contexto(
                    pregunta_texto=p.texto,
                    dificultad=dificultad,
                    respuestas_existentes=contexto,
                    instrucciones_ia=instrucciones
                )

                # Asociar respuesta generada con su id original
                respuestas_generadas = [
                    {
                        "id": instr["id"],
                        "texto": generado,
                        "corecta": instr["corecta"],
                        "ia": True
                    }
                    for generado, instr in zip(generadas, instrucciones)
                ]

                respuestas_serializadas.extend(respuestas_generadas)

            # Si no es IA, simplemente añadimos las respuestas IA ya escritas
            elif not p.ia:
                respuestas_serializadas.extend([
                    {
                        "id": r.id,
                        "texto": r.texto,
                        "corecta": r.corecta,
                        "ia": True
                    }
                    for r in respuestas_ia
                ])

            resultado.append({
                "id": p.id,
                "texto": p.texto,
                "respuestas": respuestas_serializadas
            })

        return resultado
