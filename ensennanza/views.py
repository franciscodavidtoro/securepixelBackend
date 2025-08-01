from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)


from .serializers import CursoSerializers, TemaSerializers
from .models import Curso, Tema
from preguntas.models import Prueba

from rest_framework.views import APIView
from rest_framework.response import Response

class CursoCrearListarAPI(ListCreateAPIView):
    queryset=Curso.objects.all()
    serializer_class=CursoSerializers
    
class CursoLeerActualizarEliminarAPI(RetrieveUpdateDestroyAPIView):
    queryset=Curso.objects.all()
    serializer_class=CursoSerializers


class TemaCrearListarAPI(ListCreateAPIView):
    queryset=Tema.objects.all()
    serializer_class=TemaSerializers

class TemaLeerActualizarEliminarAPI(RetrieveUpdateDestroyAPIView):
    queryset=Tema.objects.all()
    serializer_class=TemaSerializers
    

#Obtener Siguiente tema:
class TemaSiguiente(APIView):
    #busca las pruevas completadas y va al siguiente a ese
    #si no tiene pruevas va al tema con el orden mas bajo
    #si ya no ay temas siguientes devuelve vacio
    def get(self, request, *args, **kwargs):
        usuario = request.user
        UltimaPrueba = Prueba.objects.filter(usuario=usuario).order_by('-fecha').first()
        ultimo_tema = UltimaPrueba.tema if UltimaPrueba else None
        if ultimo_tema:
            siguiente_tema = Tema.objects.filter(orden__gt=ultimo_tema.orden).order_by('orden').first()
        else:
            siguiente_tema = Tema.objects.order_by('orden').first()
            
        if siguiente_tema:
            serializer = TemaSerializers(siguiente_tema)
            return Response(serializer.data, status=200)
        return Response({'detail': 'No hay más temas disponibles.'}, status=404)
        