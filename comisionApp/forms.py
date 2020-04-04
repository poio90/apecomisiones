from django import forms
from .models import Anticipo,Transporte


class SolicitudForm(forms.Form):
    """ Formulario para validar los campos de la solicitud """
    motivo = forms.CharField(
        min_length=6,
        required=True
    )

    fech_inicio = forms.CharField(
        required=True
    )

    duracion_prevista = forms.CharField(
        min_length=2,
        max_length=10,
        required=True
    )

    ciudad = forms.CharField(
        required=True
    )

    transporte = forms.CharField(
        required=True
    )

    patente = forms.CharField(
        required=True
    )

    gastos_previstos = forms.CharField(
        min_length=2,
        max_length=10,
        required=True
    )


class Anticipo(forms.ModelForm):
    class Meta:
        model: Anticipo

class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo','patente']
