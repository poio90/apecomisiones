from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Afiliado

class DateInput(DatePickerInput):
    def __init__(self):
        DatePickerInput.__init__(self,format="%Y-%m-%d")

class FormularioRegistro(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['num_afiliado'].widget.attrs['placeholder'] = 'Número de Afiliado'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repetir contraseña'

    class Meta:
        model = Afiliado
        fields = ['username', 'email',
                  'num_afiliado', 'password1', 'password2']
        widget = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'num_afiliado': forms.TextInput(),
            'password1': forms.TextInput(),
            'password2': forms.TextInput(),
        }


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class AgenteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Apellido'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nombre'
        self.fields['num_afiliado'].widget.attrs['placeholder'] = 'Numero de afiliado'
        self.fields['fecha_nacimiento'].widget.attrs['placeholder'] = 'Fecha nacimiento'
        self.fields['num_tel'].widget.attrs['placeholder'] = 'Número de telefono'
        self.fields['dni'].widget.attrs['placeholder'] = 'DNI'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

    class Meta:
        model = Afiliado
        fields = ['last_name', 'first_name', 'num_afiliado',
                  'fecha_nacimiento', 'num_tel', 'dni', 'email']
        widget = {
            'last_name': forms.TextInput(),
            'first_name': forms.TextInput(),
            'num_afiliado': forms.TextInput(),
            'fecha_nacimiento':  DatePickerInput(options={'format': 'YYYY-MM-DD', 'debug': True}).start_of('event active days'),
            'dni': forms.TextInput(),
            'email': forms.EmailInput()
        }
