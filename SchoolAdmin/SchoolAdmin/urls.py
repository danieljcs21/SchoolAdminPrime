"""SchoolAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from school_app.views import *
from school_app.facade import *
from school_app.api import *
from django.contrib.auth.decorators import   *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #BASE
    path('', IndexPageView.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('accounts/login/', SchoolLoginView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path('obtain_auth_token/', obtain_auth_token, name='obtain_auth_token'),
    path('home/', TemplateView.as_view(template_name="bases/base.html"), name="home"),
    #API
    path('api_login/', api_login, name='api_login'),
    path('api_crear_estudiante/', SchoolCrearEstudiante.as_view(), name='api_crear_estudiante'),
    path('api_crear_editar_estudiantes/', SchoolCrearEditarEstudiante.as_view(), name='api_crear_editar_estudiantes'),
    path('api_consultar_estudiantes/', SchoolConsultarEstudiante.as_view(), name='api_consultar_estudiantes'),
    path('api_eliminar_estudiantes/', SchoolEliminarEstudiante.as_view(), name='api_eliminar_estudiantes'),
    path('api_datos_estudiantes/', SchoolConsultarDatosEstudiante.as_view(), name='api_datos_estudiantes'),
    #PAGES
    path('consultar_cursos/', ConsultarCursosView.as_view(), name='consultar_cursos'),
    path('consultar_estudiantes/', ConsultarEstudiantesView.as_view(), name='consultar_estudiantes'),
    path('estudiante_curso/<int:estudiante_id>/', EstudianteCursoView.as_view(), name='estudiante_curso'),
    #AJAX
    path('ajax/add_curso/', add_curso_ajax, name='add_curso_ajax'),
    path('ajax/get_info_curso/', get_info_curso, name='get_info_curso'),
    path('ajax/delete_curso_ajax/', delete_curso, name='delete_curso_ajax'),

    path('ajax/get_direcciones', get_direcciones, name='get_direcciones'),
    path('ajax/get_data_direccion', get_data_direccion, name='get_data_direccion'),
    path('ajax/create_edit_direccion', create_edit_direccion, name='create_edit_direccion'),
    path('ajax/delete_direccion', delete_direccion, name='delete_direccion'),

    path('ajax/add_estudiante_curso_ajax', add_estudiante_curso_ajax, name='add_estudiante_curso_ajax'),
    path('ajax/get_info_estudiante_curso', get_info_estudiante_curso, name='get_info_estudiante_curso'),
    path('ajax/delete_estudiante_curso', delete_estudiante_curso, name='delete_estudiante_curso'),
]
