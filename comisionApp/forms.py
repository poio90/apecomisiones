from django import forms
from .models import Agente,Transporte


class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'num_tel', 'email']


class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo','patente']
