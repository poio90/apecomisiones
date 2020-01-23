from django import forms
from .models import Comision,Transporte


class ComisionForm(forms.ModelForm):
    class Meta:
        model = Comision
        fields = ['id_comision','fech_inicio','fech_fin','gastos']

class RendicionComision(forms.ModelForm):
    class Meta:
        model: Comision

class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo','patente']
