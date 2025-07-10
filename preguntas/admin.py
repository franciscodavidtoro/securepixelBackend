
# Register your models here.
from django.contrib import admin

from .models import subirImg, pregunta, respuesta



class CRUDPreguntaRespuesta(admin.TabularInline):
    model=respuesta
    extra=2

class andminPreguntas(admin.ModelAdmin):
    inlines=[CRUDPreguntaRespuesta]

admin.site.register(pregunta,andminPreguntas)


admin.site.register(subirImg)  


