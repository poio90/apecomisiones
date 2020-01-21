from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Afiliado


class FormRegistro(forms.Form):

    num_afiliado = forms.CharField(min_length=7, max_length=7)
    username = forms.CharField(min_length=4, max_length=50)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())
    email = forms.CharField(min_length=6, max_length=70,
                            widget=forms.EmailInput())

    def clean_num_afliado(self):
        num_afiliado = self.cleaned_data['num_afiliado']
        num_afiliado_taken = Afiliado.objects.filter(
            num_afiliado__iexact=num_afiliado).exists()
        if num_afiliado_taken:
            raise forms.ValidationError(
                'Ya existe un usuario con este número de afiliado.')
        return num_afiliado

    def clean_username(self):
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(
            username__iexact=username).exists()
        if username_taken:
            raise forms.ValidationError(
                'Ya existe un usuario con este nombre de usuario.')
        return username

    def clean_num_afliado(self):
        email = self.cleaned_data['email']
        email_taken = User.objects.filter(email__iexact=email).exists()
        if email_taken:
            raise forms.ValidationError('Ya existe un usuario con este email.')
        return email


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


"""class DateInput(DatePickerInput):
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
        fields = ['num_afiliado', 'password1', 'password2']
        widget = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'num_afiliado': forms.TextInput(),
            'password1': forms.TextInput(),
            'password2': forms.TextInput(),
        }





class AgenteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
        self.fields['num_afiliado'].widget.attrs['placeholder'] = 'Numero de afiliado'
        self.fields['num_afiliado'].widget.attrs['readonly'] = 'readonly'
        self.fields['num_tel'].widget.attrs['placeholder'] = 'Número de telefono'
        self.fields['dni'].widget.attrs['placeholder'] = 'DNI'

    class Meta:
        model = Afiliado
        fields = ['num_afiliado', 'num_tel', 'dni']

        widget = {
            'last_name': forms.TextInput(),
            'first_name': forms.TextInput(),
            'num_afiliado': forms.TextInput(),
            'dni': forms.TextInput(),
            'email': forms.EmailInput()
        }"""
