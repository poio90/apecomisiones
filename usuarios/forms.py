from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class FormRegistro(forms.Form):

    username = forms.CharField(
        min_length=4,
        max_length=50
    )

    num_afiliado = forms.CharField(
        min_length=5,
        max_length=7
    )
    
    dni = forms.CharField(
        min_length=7,
        max_length=8
    )

    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )
    
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )

    def clean_num_afliado(self):
        """Número de afiliado debe ser unico"""
        num_afiliado = self.cleaned_data['num_afiliado']
        num_afiliado_taken = User.objects.filter(
            num_afiliado=num_afiliado).exists()
        if num_afiliado_taken:
            raise forms.ValidationError(
                'Ya existe un usuario con este número de afiliado.')
        return num_afiliado

    def clean_username(self):
        """Nombre de usuario debe ser unico"""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(
            username=username).exists()
        if username_taken:
            raise forms.ValidationError(
                'Ya existe un usuario con este nombre de usuario.')
        return username

    def clean_dni(self):
        """DNI debe ser unico"""
        dni = self.cleaned_data['dni']
        dni_taken = User.objects.filter(
            dni=dni).exists()
        if dni_taken:
            raise forms.ValidationError(
                'Ya existe un usuario con este número de documento.')
        return dni

    def clean(self):
        """Verificacion del password"""
        data = super().clean()  # forma de llamar al metodo antes de ser sobreescrito, trae los datos
        passw = data['password']
        passw_confirmation = data['password_confirmation']
        if passw != passw_confirmation:
            raise forms.ValidationError('No coincide la contraseña')
        return data


class FormLogin(AuthenticationForm):
    """ Formulario para validar los datos de login """
    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'DNI'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class FormUpdateProfile(forms.Form):
    """ Formulario para validar perfil de usuario """
    email = forms.CharField(
        min_length=6, max_length=70,
        widget=forms.EmailInput(),
        required=True
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=70,
        required=True
    )

    first_name = forms.CharField(
        min_length=2,
        max_length=70,
        required=True
    )

    dni = forms.CharField(
        min_length=8,
        max_length=8,
        required=True
    )

    num_tel = forms.CharField(
        min_length=10,
        max_length=10,
        required=True
    )


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
