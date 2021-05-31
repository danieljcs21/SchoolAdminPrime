from django.contrib import admin
from .models import *
# Register your models here.

#SE AGREGA MODELO DE CONTROL DE REGISTROS Y SE DEFINE CUALES CAMPOS VA MOSTRAR
@admin.register(Curso)
class CursoRegistroAdmin(admin.ModelAdmin):
    list_display = ()

#SE AGREGA MODELO DE CONTROL DE DETALLE Y SE DEGFINES CUALES CAMPOS VA MOSTRAR
@admin.register(Estudiante)
class EstudianteDetalleAdmin(admin.ModelAdmin):
    list_display = ()

