from django import forms
from .models import Anticipo,Transporte


class AnticipoForm(forms.ModelForm):
    class Meta:
        model = Anticipo
        fields = ['num_comision','fech_inicio','fech_fin','gastos']

class Anticipo(forms.ModelForm):
    class Meta:
        model: Anticipo

class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo','patente']
