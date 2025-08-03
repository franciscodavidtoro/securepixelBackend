from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Prueba, pregunta, respuesta
from .serializers import PruebaSerializer, PruebaConPreguntasSerializer
from inicioSesion.models import Usuario
import random


class CrearPruebaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tema_id = request.data.get("tema_id")
        dificultad = request.data.get("dificultad")
        repetible = request.data.get("repetible", False)

        # Validación básica
        if not tema_id or dificultad is None:
            return Response({"error": "tema_id y dificultad son requeridos."}, status=400)

        prueba = Prueba.objects.create(
            tema_id=tema_id,
            dificultad=dificultad,
            repetible=repetible,
            estudiante=request.user
        )

        return Response(PruebaSerializer(prueba).data, status=201)


class ObtenerPreguntasDePruebaAPIView(generics.RetrieveAPIView):
    queryset = Prueba.objects.all()
    serializer_class = PruebaConPreguntasSerializer
    permission_classes = [IsAuthenticated]


class RealizarPruebaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        prueba = Prueba.objects.get(pk=pk, estudiante=request.user)
        respuestas_usuario = request.data.get("respuestas")  # {pregunta_id: respuesta_id}
        calificacion = 0
        total = 0

        for pregunta_id, respuesta_id in respuestas_usuario.items():
            try:
                r = respuesta.objects.get(id=respuesta_id, preguntaCorespondiente_id=pregunta_id)
                if r.corecta:
                    calificacion += 1
                total += 1
            except respuesta.DoesNotExist:
                continue

        if total > 0:
            nota_final = (calificacion / total) * 10
        else:
            nota_final = 0

        prueba.realizada = True
        prueba.calificacion = nota_final
        prueba.save()

        return Response({
            "mensaje": "Prueba finalizada.",
            "calificacion": nota_final
        }, status=200)
