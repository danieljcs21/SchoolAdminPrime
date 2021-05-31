from __future__ import unicode_literals
from django.contrib.auth.forms import AuthenticationForm,authenticate
from django import forms
from .models import *
from django.contrib.auth.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import (
    Accordion, AccordionGroup, Alert, AppendedText, FieldWithButtons,
    InlineCheckboxes, InlineRadios, PrependedAppendedText, PrependedText,
    StrictButton, Tab, TabHolder,
)
# FORMULARIOS GENERADOS CORRESPONDIENTES A LOS MODELOS
class LoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username=username,password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return super(LoginForm, self).clean()

class CrearEditarCursoForm(forms.Form):
    codigo_curso = forms.CharField()
    nombre_curso = forms.CharField()
    fecha_inicio = forms.DateField(
            widget = forms.TextInput(
                attrs={'type': 'date'}
            )
        )
    fecha_fin = forms.DateField(
            widget = forms.TextInput(
                attrs={'type': 'date'}
            )
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('codigo_curso', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
                Column(Field('nombre_curso', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
                Column(Field('fecha_inicio', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
                Column(Field('fecha_fin', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
            )
        )



class CrearEditarEstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = ('FechaCreacion','FechaActualizacion')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["FechaNacimento"] = forms.DateField(
            widget = forms.TextInput(
                attrs={'type': 'date'}
            )
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
             Row(
                Column(Field('Nombres', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
                Column(Field('Apellidos', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
                Column(Field('FechaNacimento', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
                Column(Field('Genero', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
            ),
        )


class CrearEditarDireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        exclude = ('FechaCreacion','FechaActualizacion','Estudiante')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
             Row(
                Column(Field('Direccion', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
                Column(Field('TipoDireccion', css_class="form-control form-control-sm"), css_class='form-group col-md-6 '),
            ),
        )

class CrearEditarEstudianteCursoForm(forms.ModelForm):
    class Meta:
        model = EstudianteCurso
        exclude = ('FechaCreacion','FechaActualizacion','Estudiante')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
             Row(
                Column(Field('Curso', css_class="form-control form-control-sm"), css_class='form-group col-md-12 '),
            ),
        )