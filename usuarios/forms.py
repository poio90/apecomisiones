from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class FormLogin(AuthenticationForm):
    """ Formulario para validar los datos de login """
    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['autocomplete'] = 'off'
        self.fields['username'].widget.attrs['placeholder'] = 'DNI'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class FormUpdateProfile(forms.ModelForm):
    """ Formulario para validar los datos de usuario """
    class Meta:
        model = User
        fields = ['last_name','first_name','dni','email','num_tel']


class FormRegistro(UserCreationForm):
    """ Formulario para validar los datos de registro """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].widget.attrs['autocomplete'] = 'off'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['dni'].widget.attrs['placeholder'] = 'DNI'
        self.fields['num_afiliado'].widget.attrs['placeholder'] = 'Número de Afiliado'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'

    class Meta:
        model = User
        fields = ['username','num_afiliado','dni','password1', 'password2']


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = ['last_name','first_name','num_afiliado']