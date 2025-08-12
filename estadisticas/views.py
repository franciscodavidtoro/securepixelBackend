from django.shortcuts import render
from inicioSesion.models import Usuario
from preguntas.models import Prueba
from AI.models import atencion, emociones
from ensennanza.models import Curso
from rest_framework.permissions import IsAuthenticated
from typing import List

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
        



class ReporteEstadisticasGeneralesAPIView(APIView):
    """ Las estadisticas de 
    n de estudiantes
    promedios
    n de leciones repetidas
    tiempos promedio de estudio 
    del:total,filtrado por curso,profesor"""
    permission_classes = [IsAuthenticated]

    def estadisicas(usuarios: List[Usuario]) -> dict:
        """saca las estadisticas de la lista de usuarios"""
        n_estudiantes = len(usuarios)
        promedios = []
        n_lecciones = 0
        tiempos_estudio = []

        for usuario in usuarios:
            pruebas = Prueba.objects.filter(estudiante=usuario)
            if pruebas.exists():
                calificaciones = [prueba.calificacion for prueba in pruebas]
                promedios.append(sum(calificaciones) / len(calificaciones))
                n_lecciones += pruebas.filter(repetible=True).count()
            iaEnsenanza = atencion.objects.filter(usuario=usuario)
            if iaEnsenanza.exists():
                tiempos_estudio.extend([ia.tiempoLectura for ia in iaEnsenanza])

        promedio_general = sum(promedios) / len(promedios) if promedios else 0
        tiempo_promedio_estudio = sum(tiempos_estudio) / len(tiempos_estudio) if tiempos_estudio else 0

        return {
            "n_estudiantes": n_estudiantes,
            "promedio_general": promedio_general,
            "n_lecciones": n_lecciones,
            "tiempo_promedio_estudio": tiempo_promedio_estudio
        }

    def get(self, request, *args, **kwargs):
        todosEstudiantes = Usuario.objects.filter(tipo_usuario='alumno')
        profesores= Usuario.objects.filter(tipo_usuario='profesor')
        todosCursos = Curso.objects.all()
        
        estadisticasGlovales = self.estadisicas(todosEstudiantes)
        estadisticasPorCurso = {}
        for curso in todosCursos:
            estudiantesCurso = Usuario.objects.filter(curso=curso, tipo_usuario='alumno')
            estadisticasPorCurso[curso.nombre] = self.estadisicas(estudiantesCurso)
        estadisticasPorProfesor = {}
        for profesor in profesores:
            cursosProfesor = Curso.objects.filter(profesor=profesor)
            estudiantesProfesor=[]
            for curso in cursosProfesor:
                estudiantesCurso = Usuario.objects.filter(curso=curso, tipo_usuario='alumno')
                estudiantesProfesor.extend(estudiantesCurso)
            estadisticasPorProfesor[profesor.nombre] = self.estadisicas(estudiantesProfesor)
        return Response({
            "estadisticas_globale": estadisticasGlovales,
            "estadisticas_por_curso": estadisticasPorCurso,
            "estadisticas_por_profesor": estadisticasPorProfesor
        })
        
class ReporteEmocionesEstudiantesAPIView(APIView):
    """Reporte de emociones de los estudiantes obteniendo porcentaje de emociones y los promedios de las pruevas."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        emociones_estudiantes = emociones.objects.all()
        if not emociones_estudiantes.exists():
            return Response({"error": "No hay emociones registradas"}, status=404)
        emociones_totales = {}
        for emocion in emociones_estudiantes:
            emociones_totales[emocion.emocionPredominante] = emociones_totales.get(emocion.emocionPredominante, 0) + 1
            
        total_emociones = sum(emociones_totales.values())
        emociones_porcentaje = {emocion: (cantidad / total_emociones) * 100 for emocion, cantidad in emociones_totales.items()}
        
        # Calcular el promedio de calificaciones dependiendo de la emoción predominante
        promedios_calificaciones = {}
        for key, value in emociones_porcentaje.items():
            EmocionesPorEmocion = emociones.objects.filter(emocionPredominante=key)
            if EmocionesPorEmocion.exists():
                calificaciones = Prueba.objects.filter(emociones__in=EmocionesPorEmocion).values_list('calificacion', flat=True)
                if calificaciones:
                    promedios_calificaciones[key] = sum(calificaciones) / len(calificaciones)
                else:
                    promedios_calificaciones[key] = 0
        
        return Response({
            "emociones_porcentaje": emociones_porcentaje,
            "promedios_calificaciones": promedios_calificaciones
        })
    