import ast,json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.http import HttpResponse , HttpResponseRedirect,JsonResponse
from .models import *
import requests
import datetime
from datetime import datetime
# from rest_framework import serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate
from rest_framework import status
from django.forms.models import model_to_dict
import time
import os
urlk = "http://127.0.0.1:8000"
# API PARA LOGEO LA CUAL ARROJA EL TOKEN
@api_view(['POST'])
def api_login(request):
    data = {}
    try:
        alias = request.POST.get('alias')
        password= request.POST.get('password')

        if(alias != None, password != None):

            user = authenticate(username=alias, password=password)

            if(user):
                url = urlk+'/obtain_auth_token/'
                payload = {'username': alias, 'password':password}
                headers = {'Content-type':'application/json'}
                r = requests.post(url ,data=payload)
                r = json.loads(r.text)

                data['token'] = r['token']
                data['mensaje'] = 'BIENVENIDO'
                data['login'] = True
                data['data'] = model_to_dict(user)
                return JsonResponse( data,safe=False)
            else:
                data['token'] = ''
                data['mensaje'] = 'CREDENCIALES INVALIDAS'
                data['login'] = False
                data['data'] = {}
                return JsonResponse( data,safe=False)
        else:
            data['token'] = ''
            data['mensaje'] = 'VACIO'
            data['login'] = False
            data['data'] = {}
            return JsonResponse(data,safe=False)
    except Exception as err:
        data['token'] = ''
        data['mensaje'] = 'ERROR'
        data['login'] = False
        data['data'] = {}
        date = datetime.now().date()
        timestr = time.strftime("%Y%m%d-%H%M%S")
        path = "logs"
        file_name = "api_login-"+str(date),timestr+".txt"
        completeName = os.path.join(str(path), str(file_name))
        f = open(str(completeName), "w")
        f.write(str(err))
        f.close()
    return JsonResponse(data,safe=False)
# API PARA CREAR ESTUDIANTE (NO EDITA)
class SchoolCrearEstudiante(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = {}
        try:
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            genero = request.POST.get('genero')

            estudiante = Estudiante()
            estudiante.Nombres = nombres
            estudiante.Apellidos = apellidos
            estudiante.FechaNacimento = fecha_nacimiento
            estudiante.Genero = genero
            estudiante.save()

            data['error'] = False
            data['mensaje'] = 'Estudiante creado correctamente'
            data['data'] = model_to_dict(estudiante)

        except Exception as err:
            data['error'] = True
            data['mensaje'] = 'Ha ocurrido un error'
            data['data'] = {}
            date = datetime.now().date()
            timestr = time.strftime("%Y%m%d-%H%M%S")
            path = "logs"
            file_name = "SchoolCrearEstudiante-"+str(date),timestr+".txt"
            completeName = os.path.join(str(path), str(file_name))
            f = open(str(completeName), "w")
            f.write(str(err))
            f.close()

        return JsonResponse(data,safe=False)
# API APRA CREAR Y EDITAR ESTUDAINTE
class SchoolCrearEditarEstudiante(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = {}
        try:
            id = request.POST.get('id')
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            genero = request.POST.get('genero')

            if id != '':
                estudiante = Estudiante.objects.get(id = id)
            else:
                estudiante = Estudiante()

            estudiante.Nombres = nombres
            estudiante.Apellidos = apellidos
            estudiante.FechaNacimento = fecha_nacimiento
            estudiante.Genero = genero
            estudiante.save()

            data['error'] = False
            data['mensaje'] = 'Estudiante creado-editado correctamente'
            data['data'] = model_to_dict(estudiante)

        except Exception as err:
            data['error'] = True
            data['mensaje'] = 'Ha ocurrido un error'
            data['data'] = {}
            date = datetime.now().date()
            timestr = time.strftime("%Y%m%d-%H%M%S")
            path = "logs"
            file_name = "SchoolCrearEditarEstudiante-"+str(date),timestr+".txt"
            completeName = os.path.join(str(path), str(file_name))
            f = open(str(completeName), "w")
            f.write(str(err))
            f.close()

        return JsonResponse(data,safe=False)
# API PARA ELIMINAR UN ESTUDIANTE
class SchoolEliminarEstudiante(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = {}
        try:
            id = request.POST.get('id')

            Direccion.objects.filter(Estudiante_id=id).delete()
            Estudiante.objects.filter(id=id).delete()

            data['error'] = False
            data['mensaje'] = 'Estudiante eliminado correctamente'
            data['data'] = {}

        except Exception as err:
            data['error'] = True
            data['mensaje'] = 'Ha ocurrido un error'
            data['data'] = {}
            date = datetime.now().date()
            timestr = time.strftime("%Y%m%d-%H%M%S")
            path = "logs"
            file_name = "SchoolEliminarEstudiante-"+str(date),timestr+".txt"
            completeName = os.path.join(str(path), str(file_name))
            f = open(str(completeName), "w")
            f.write(str(err))
            f.close()

        return JsonResponse(data,safe=False)
# API PARA CONSULTAR TODOS LOS ESTUDIANTES
class SchoolConsultarEstudiante(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = {}
        objeto_resp = {}
        objeto_resp['data_estudiantes'] = []
        try:

            estudiantes = Estudiante.objects.all().order_by('id')
            for item in estudiantes:
                item.Genero = item.get_Genero_display()
                objeto_resp['data_estudiantes'].append(model_to_dict(item)) # SE AGREGA A LA LISTA

            data['error'] = False
            data['mensaje'] = 'Listado de estudiantes'
            data['data'] = objeto_resp

        except Exception as err:
            data['error'] = True
            data['mensaje'] = 'Ha ocurrido un error'
            data['data'] = {}
            date = datetime.now().date()
            timestr = time.strftime("%Y%m%d-%H%M%S")
            path = "logs"
            file_name = "SchoolConsultarEstudiante-"+str(date),timestr+".txt"
            completeName = os.path.join(str(path), str(file_name))
            f = open(str(completeName), "w")
            f.write(str(err))
            f.close()

        return JsonResponse(data,safe=False)
# API PARA CONSULTAR LOS DATOS DE UN ESTUDIANTE
class SchoolConsultarDatosEstudiante(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = {}
        objeto_resp = {}
        objeto_resp['data_estudiantes'] = []
        try:
            id = request.POST.get('id')

            estudiante = Estudiante.objects.get(id = id)
            data['error'] = False
            data['mensaje'] = 'Datos de estudiante'
            data['data'] = model_to_dict(estudiante)

        except Exception as err:
            data['error'] = True
            data['mensaje'] = 'Ha ocurrido un error'
            data['data'] = {}
            date = datetime.now().date()
            timestr = time.strftime("%Y%m%d-%H%M%S")
            path = "logs"
            file_name = "SchoolConsultarDatosEstudiante-"+str(date),timestr+".txt"
            completeName = os.path.join(str(path), str(file_name))
            f = open(str(completeName), "w")
            f.write(str(err))
            f.close()

        return JsonResponse(data,safe=False)


