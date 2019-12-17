from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Afiliado

class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #clave = self.labels.keys()
        #valor = self.labels.values()
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = User
        fields = ['last_name','first_name','email']
        labels = {
            'last_name':'Apellido',
            'first_name':'Nombre',
            'email':'Email',
        }
        widget= {
            'last_name': forms.TextInput(
                attrs = {
                    'placeholder':'Apellido'
                }

            ),
            'first_name': forms.TextInput(
                attrs = {
                    'placeholder':'Nombre'
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'placeholder':'Email'
                }
            )
        }

class AgenteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
    class Meta:
        model = Afiliado
        fields = ['last_name','num_afiliado','fecha_nacimiento','num_tel','dni']
        labels = {
            'last_name':'Apellido',
            'num_afiliado':'Número de afiliado',
            'fecha_nacimiento':'Fecha de nacimiento',
            'num_tel':'Número de telefono',
            'dni':'DNI'
        }
        widget = {
            'last_name': forms.TextInput(
                attrs = {
                    'placeholder':'Apellido'
                }
            ),
            'num_afiliado': forms.TextInput(
                attrs = {
                    'placeholder':'Numero de afiliado'
                }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs = {
                    'placeholder':'Fecha nacimiento'
                }
            ),
            'dni': forms.TextInput(
                attrs = {
                    'placeholder':'DNI'
                }
            )
        }
    