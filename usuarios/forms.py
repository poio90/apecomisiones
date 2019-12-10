from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Agente

class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class UserForm(forms.ModelForm):
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
                    'class':'form-control',
                    'placeholder':'Apellido'
                }

            ),
            'first_name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Nombre'
                }
            ),
            'email': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Email'
                }

            )
        }

class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['num_afiliado','fecha_nacimiento','num_tel','dni']
        labels = {
            'num_afiliado':'Número de afiliado',
            'fecha_nacimiento':'Fecha de nacimiento',
            'num_tel':'Número de telefono',
            'dni':'DNI'
        }
        widget= {
            'num_afiliado': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Numero de afiliado'
                }

            ),
            'fecha_nacimiento': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Fecha nacimiento'
                }
            ),
            'dni': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'DNI'
                }
            )
        }
    