from django import forms
from .models import Agente,Comision,Transporte


class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['num_afiliado','nombre', 'apellido', 'dni', 'fecha_nacimiento', 'num_tel', 'email']

class ComisionForm(forms.ModelForm):
    class Meta:
        model = Comision
        fields = ['id_comision','fech_inicio','fech_fin','gasto']

class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo','patente']
