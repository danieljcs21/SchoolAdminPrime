from django.db import models

# Create your models here.

class Curso(models.Model):
    CodigoCurso = models.CharField(max_length=250)
    NombreCurso = models.CharField(max_length=250)
    FechaInicio = models.DateTimeField()
    FechaFin =  models.DateTimeField()
    FechaCreacion = models.DateTimeField(auto_now_add=True, auto_now=False)
    FechaActualizacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.CodigoCurso) +" - "+ self.NombreCurso

class Estudiante(models.Model):
    GENERO = [
        (0,"Femenino"),
        (1,"Masculino"),
        (2,"NoDefinido"),
        ]
    Nombres = models.CharField(max_length=300)
    Apellidos = models.CharField(max_length=300)
    FechaNacimento = models.DateTimeField()
    Genero =  models.IntegerField(choices=GENERO)
    FechaCreacion = models.DateTimeField(auto_now_add=True, auto_now=False)
    FechaActualizacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Nombres +" "+ self.Apellidos

class Direccion(models.Model):
    TIPOS_DIRECCION = [
        (0,"Domicilio"),
        (1,"Laboral"),
        (2,"Temporal"),
        ]
    Direccion = models.CharField(max_length=500)
    Estudiante = models.ForeignKey(Estudiante, default = 1, on_delete=models.PROTECT)
    TipoDireccion =  models.IntegerField(choices=TIPOS_DIRECCION)
    FechaCreacion = models.DateTimeField(auto_now_add=True, auto_now=False)
    FechaActualizacion = models.DateTimeField(auto_now=True)

class Entidad(models.Model):
    EstaBorrado = models.BooleanField()
    FechaCreacion = models.DateTimeField(auto_now_add=True, auto_now=False)
    FechaBorrado = models.DateTimeField()
    FechaActualizacion = models.DateTimeField(auto_now=True)

class EstudianteCurso(models.Model):
    Estudiante = models.ForeignKey(Estudiante, default = 1, on_delete=models.PROTECT)
    Curso = models.ForeignKey(Curso, default = 1, on_delete=models.PROTECT)
    FechaCreacion = models.DateTimeField(auto_now_add=True, auto_now=False)
    FechaActualizacion = models.DateTimeField(auto_now=True)

class DoWork(models.Model):
    EstaBorrado = models.BooleanField(default=True)
    Evento = models.CharField(max_length=500)
    Fecha = models.DateTimeField(auto_now_add=True, auto_now=False)

