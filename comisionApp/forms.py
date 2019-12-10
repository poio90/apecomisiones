from django import forms
from .models import Comision,Transporte




class ComisionForm(forms.ModelForm):
    class Meta:
        model = Comision
        fields = ['id_comision','fech_inicio','fech_fin','gasto']

class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo','patente']
