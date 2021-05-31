from django.shortcuts import render
from django.views.generic import CreateView,UpdateView,ListView,View,TemplateView,FormView,RedirectView
from django.contrib.auth.views import LoginView
from .forms import *
from .api import *
from django.views.generic import TemplateView
#LOGIN
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import *
from django.conf import settings
from urllib.parse import unquote
from django.db import connection,connections
from rest_framework.authtoken.models import *
import threading

# DOWORK QUE TRABAJA EN SEGUNDO PLANO SIN INTERRUMPIR LAS DEMAS OPERACIONES EN LA APLICACION
def doWork(): 
    do_work = DoWork()
    do_work.Evento = 'message'
    do_work.save()
    threading.Timer(10.0, doWork).start()
# doWork()



urlk = "http://127.0.0.1:8000"
class IndexPageView(RedirectView):
    pattern_name="login"

class SchoolLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = LoginForm

class ConsultarCursosView(LoginRequiredMixin, FormView):
    http_method_names = ['get','post']
    form_class = CrearEditarCursoForm
    template_name = 'pages/consultar_cursos.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CrearEditarCursoForm()
        context['data'] = Curso.objects.all().order_by('NombreCurso')
        return context

class ConsultarEstudiantesView(LoginRequiredMixin, FormView):
    http_method_names = ['get','post']
    form_class = CrearEditarEstudianteForm
    template_name = 'pages/consultar_estudiantes.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CrearEditarEstudianteForm() 
        context['filter_form_direccion'] = CrearEditarDireccionForm() 
        id_user = self.request.user.id
        token = Token.objects.get(user_id = id_user)
        myurl = urlk + "/api_consultar_estudiantes/"
        response = requests.post(myurl, headers={'Authorization': 'Token {}'.format(token)})
        data = response.json()
        context['data'] = data['data']['data_estudiantes']
        context['token'] = token
        return context

class EstudianteCursoView(TemplateView):
    http_method_names = ['get','post']
    template_name = 'pages/consultar_estudiante_curso.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estudiante_id =  int(self.kwargs['estudiante_id'])
        context['data'] = EstudianteCurso.objects.filter(Estudiante_id = estudiante_id)
        context['estudiante_id'] =estudiante_id
        context['filter_form'] = CrearEditarEstudianteCursoForm()
        return context