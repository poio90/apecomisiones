from django import forms
from .models import Agente,Comision,Transporte


class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['num_afiliado', 'dni', 'fecha_nacimiento', 'num_tel']
        labels = {
            'num_afiliado': 'Número de afiliado',
            'dni': 'DNI',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'num_tel': 'Numero de telefono',
        }

class ComisionForm(forms.ModelForm):
    class Meta:
        model = Comision
        fields = ['id_comision','fech_inicio','fech_fin','gasto']

class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo','patente']
