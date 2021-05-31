from school_app.models import *
from school_app.views import *
from django.http import HttpResponse , HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import *
from django.db import connection,connections
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.core import serializers
import datetime
import os
import sys
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from datetime import datetime
from django.forms.models import model_to_dict
# aARCHIVO EL CUAL CONTIENE TODAS LAS FUNCIONES USADAS POR AJAX EN LOS HTML
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def add_curso_ajax(request):
    respuesta = {}
    respuesta['mensaje'] = ""
    respuesta['campo'] = "Aviso"

    codigo_curso = request.POST.get('codigo_curso')
    nombre_curso = request.POST.get('nombre_curso')
    fecha_inicio = request.POST.get('fecha_inicio')
    fecha_fin = request.POST.get('fecha_fin')
    id_curso = request.POST.get('id_curso')
    try:

        verify_curso_exist = Curso.objects.filter(CodigoCurso=codigo_curso)
        if id_curso == '':
            curso = Curso()
            if verify_curso_exist:
                respuesta['mensaje'] = "Codigo ya existe"
                respuesta['campo'] = "Codigo"
                return JsonResponse(respuesta)
        else:
            curso = Curso.objects.get(pk=id_curso)

        curso.CodigoCurso = codigo_curso
        curso.NombreCurso = nombre_curso
        curso.FechaInicio = fecha_inicio
        curso.FechaFin = fecha_fin
        curso.save()
        respuesta['mensaje'] = "Curso Creado-Editado Correctamente"
        respuesta['campo'] = "Correcto"

    except Exception as error:
        respuesta['mensaje'] = str(error)
        respuesta['campo'] = "ERROR"
    return JsonResponse(respuesta)

def get_info_curso(request):
    respuesta = {}

    id_curso = request.POST.get('id_curso')
    curso = Curso.objects.get(id = id_curso)
    respuesta['data'] = model_to_dict(curso)

    return JsonResponse(respuesta,safe=False)

def delete_curso(request):
    respuesta = {}
    id_curso = request.POST.get('id_curso')
    try:
        Curso.objects.filter(id=id_curso).delete()
        respuesta['mensaje'] = "Curso Eliminado Correctamente"
        respuesta['campo'] = "Correcto"
    except Exception as error:
        respuesta['mensaje'] = 'EL CURSO TIENE ESTUDIANTES ASOCIADOS'
        respuesta['campo'] = "ERROR"

    return JsonResponse(respuesta,safe=False)


def add_estudiante_curso_ajax(request):
    respuesta = {}
    respuesta['mensaje'] = ""
    respuesta['campo'] = "Aviso"

    id_estudiante_curso = request.POST.get('id_estudiante_curso')
    id_curso = request.POST.get('id_curso')
    id_estudiante = request.POST.get('id_estudiante')

    try:

        verify_curso_exist = EstudianteCurso.objects.filter(Estudiante_id=id_estudiante, Curso_id=id_curso)
        if id_estudiante_curso == '':
            estudiante_curso = EstudianteCurso()
            estudiante_curso.Estudiante_id = id_estudiante
            if verify_curso_exist:
                respuesta['mensaje'] = "Relacion ya existe ya existe"
                respuesta['campo'] = "Relacion ya existe"
                return JsonResponse(respuesta)
        else:
            estudiante_curso = EstudianteCurso.objects.get(pk=id_estudiante_curso)

        estudiante_curso.Curso_id = id_curso
        estudiante_curso.save()
        respuesta['mensaje'] = "Relacion Creado-Editado Correctamente"
        respuesta['campo'] = "Correcto"

    except Exception as error:
        respuesta['mensaje'] = str(error)
        respuesta['campo'] = "ERROR"
    return JsonResponse(respuesta)

def get_info_estudiante_curso(request):
    respuesta = {}

    id_estudiante_curso = request.POST.get('id_estudiante_curso')
    curso = EstudianteCurso.objects.get(id = id_estudiante_curso)
    respuesta['data'] = model_to_dict(curso)

    return JsonResponse(respuesta,safe=False)

def delete_estudiante_curso(request):
    respuesta = {}
    id_estudiante_curso = request.POST.get('id_estudiante_curso')
    EstudianteCurso.objects.filter(id=id_estudiante_curso).delete()
    respuesta['mensaje'] = "Relacion Eliminada Correctamente"
    respuesta['campo'] = "Correcto"

    return JsonResponse(respuesta,safe=False)



def get_direcciones(request):
    respuesta = {}
    estudiante_id = request.POST.get('estudiante_id')
    with connection.cursor() as cursor:
        cursor.execute("exec sp_school_get_direcciones @EstudianteId = %s",[estudiante_id])
        result = dictfetchall(cursor)
    respuesta['data'] = result
    return JsonResponse(respuesta,safe=False)

def get_data_direccion(request):
    respuesta = {}
    direccion_id = request.POST.get('direccion_id')
    with connection.cursor() as cursor:
        cursor.execute("exec sp_school_get_data_direccion @DireccionId = %s",[direccion_id])
        result = dictfetchall(cursor)
    respuesta['data'] = result
    return JsonResponse(respuesta,safe=False)

def create_edit_direccion(request):
    respuesta = {}
    direccion_id = request.POST.get('direccion_id')
    direccion = request.POST.get('direccion')
    estudiante_id = request.POST.get('estudiante_id')
    tipo_direccion = request.POST.get('tipo_direccion')


    with connection.cursor() as cursor:
        if direccion_id == '':
            cursor.execute("exec sp_school_create_edit_direcciones @Direccion = '{0}', @TipoDireccion = {1}, @EstudianteId = {2}".format(direccion,tipo_direccion,estudiante_id))
        else:
            cursor.execute("exec sp_school_create_edit_direcciones @DireccionId = {0}, @Direccion = '{1}', @TipoDireccion = {2}, @EstudianteId = {3}".format(direccion_id,direccion,tipo_direccion,estudiante_id))
    respuesta['data'] = {}
    respuesta['data'] = 'direccion creada-editada correctamente'
    return JsonResponse(respuesta,safe=False)

def delete_direccion(request):
    respuesta = {}
    direccion_id = request.POST.get('direccion_id')
    with connection.cursor() as cursor:
        cursor.execute("exec sp_school_delete_direccion @DireccionId = %s",[direccion_id])
    respuesta['data'] = {}
    respuesta['mensaje'] = 'elimidado correctamente'
    return JsonResponse(respuesta,safe=False)
































