from django.shortcuts import render
from inicioSesion.models import Usuario
from preguntas.models import Prueba
from AI.models import atencion, emociones
from ensennanza.models import Curso
from rest_framework.permissions import IsAuthenticated


from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone


class AdminDasboardEstadisticasAPIView(APIView):
    """Vista para obtener estadísticas del dashboard de administración.
    n_usuarios 
    n pruevas completadas
    n y no completadas 
    uptime
    nota promedio
    n cursos

    """
    def get(self, request, *args, **kwargs):
        # Obtener el número de usuarios
        n_usuarios = Usuario.objects.filter(tipo_usuario='alumno').count()

        # Obtener el número de pruebas completadas y no completadas
        n_pruebas_completadas = Prueba.objects.filter(realizada=True).count()
        n_pruebas_no_completadas = Prueba.objects.filter(realizada=False).count()

        # Calcular la nota promedio de las pruebas
        notas = Prueba.objects.filter(realizada=True).values_list('calificacion', flat=True)
        nota_promedio = sum(notas) / len(notas) if notas else 0

        # Obtener el número de cursos
        n_cursos = Curso.objects.count()

        # Calcular el uptime (diferencia entre ahora y la fecha de creación del primer usuario)
        primer_usuario = Usuario.objects.order_by('fecha_creacion').first()
        uptime = timezone.now() - primer_usuario.fecha_creacion if primer_usuario else timezone.timedelta(0)

        return Response({
            "n_usuarios": n_usuarios,
            "n_pruebas_completadas": n_pruebas_completadas,
            "n_pruebas_no_completadas": n_pruebas_no_completadas,
            "nota_promedio": nota_promedio,
            "n_cursos": n_cursos,
            "uptime": uptime.total_seconds()
        })
        
        
class ProfesorDasboardEstadisticasAPIView(APIView):
    """Vista para obtener estadísticas del dashboard de administración.
    n estudiantes
    n pruevas completadas
    n y no completadas 
    n estudiantes reprobaron ultima prueva
    nota promedio
    n cursos

    """
    
    permission_classes = [isAuthenticated]
    
    def get(self, request, *args, **kwargs):
        usuario = request.user  # type: Usuario
        if usuario.tipo_usuario != "Profesor":
            return Response({'error': 'No tiene permisos'}, status=status.HTTP_401_UNAUTHORIZED)
        # Obtener el número de estudiantes del profesor
        cursos = Curso.objects.filter(profesor=usuario)
        estudiantes = Usuario.objects.filter(curso__in=cursos, tipo_usuario='alumno')
        # Obtener el número de pruebas completadas y no completadas por los estudiantes del profesor
        n_pruebas_completadas = Prueba.objects.filter(realizada=True, usuario__in=estudiantes).count()
        n_pruebas_no_completadas = Prueba.objects.filter(realizada=False, usuario__in=estudiantes).count()
        # Obtener la última prueba de cada estudiante
        ultima_pruebas = Prueba.objects.filter(usuario__in=estudiantes).order_by('-fecha_creacion').distinct('usuario')
        # Calcular el número de estudiantes que reprobaron la última prueba 
        n_estudiantes_reprobaron = sum(1 for prueba in ultima_pruebas if prueba.calificacion < 14)
        
        # Calcular la nota promedio de las pruebas de los estudiantes del profesor
        notas = Prueba.objects.filter(realizada=True, usuario__in=estudiantes).values_list('calificacion', flat=True)
        nota_promedio = sum(notas) / len(notas) if notas else 0
        # Obtener el número de cursos del profesor
        n_cursos = cursos.count()
        return Response({
            "n_estudiantes": estudiantes.count(),
            "n_pruebas_completadas": n_pruebas_completadas,
            "n_pruebas_no_completadas": n_pruebas_no_completadas,
            "n_estudiantes_reprobaron": n_estudiantes_reprobaron,
            "nota_promedio": nota_promedio,
            "n_cursos": n_cursos
        })
        



