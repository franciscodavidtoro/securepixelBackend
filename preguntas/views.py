from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Prueba, pregunta, respuesta
from .serializers import PruebaSerializer, PruebaConPreguntasSerializer
from inicioSesion.models import Usuario
from ensennanza.models import Tema
import random


from rest_framework.generics import RetrieveAPIView, ListAPIView


class ListarPruebasAPIView(ListAPIView):#listar todas las pruebas de un usuario
    serializer_class = PruebaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        return Prueba.objects.filter(estudiante=usuario).order_by('-fecha')
    
class PruebaDetalleAPIView(RetrieveAPIView):
    queryset = Prueba.objects.all()
    serializer_class = PruebaSerializer
    permission_classes = [IsAuthenticated]



class CrearPruebaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        tema_id = request.data.get("tema_id")
         # Validación básica
        if not tema_id:
            return Response({"error": "tema_id es requerido."}, status=400)

        try:
            tema = Tema.objects.get(id=tema_id)
            tema
        except Tema.DoesNotExist:
            return Response({"error": "Tema no encontrado."}, status=404)

        # Buscar pruebas anteriores del usuario en este tema
        pruebas_anteriores = Prueba.objects.filter(estudiante=request.user).order_by('-fecha') 
        ultima_prueba = pruebas_anteriores.first() 
        if not pruebas_anteriores.exists() or ultima_prueba.realizada == False:
            dificultad = tema.curso.dificultadMinima
        else:
            # type: Prueba
            if ultima_prueba.calificacion > 18:
                dificultad = min(ultima_prueba.dificultad + 1, tema.curso.dificultadMaxima)
            if ultima_prueba.calificacion < 14:
                dificultad = max(ultima_prueba.dificultad - 1, tema.curso.dificultadMinima)
            else:
                dificultad = ultima_prueba.dificultad


        prueba = Prueba.objects.create(
            tema_id=tema_id,
            dificultad=dificultad,
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
        print(respuestas_usuario)
        for r_data in respuestas_usuario:
            pregunta_id = r_data['pregunta_id']
            respuesta_id = r_data['respuesta_id']
            try:
                r = respuesta.objects.get(id=respuesta_id, preguntaCorespondiente_id=pregunta_id)
                if r.corecta:
                    calificacion += 1
                total += 1
            except respuesta.DoesNotExist:
                continue


        if total > 0:
            nota_final = (calificacion / total) * 20
        else:
            nota_final = 0

        prueba.realizada = True
        prueba.calificacion = nota_final
        prueba.save()

        return Response({
            "mensaje": "Prueba finalizada.",
            "calificacion": nota_final,
            "aprobado": nota_final >= 14,
            "respuestas_correctas": calificacion,
        }, status=200)
