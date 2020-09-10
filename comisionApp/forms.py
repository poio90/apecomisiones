from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
from .models import *
from usuarios.models import User
from usuarios.forms import UserForm


class DatePickerInput(DatePickerInput):
    options = {
        "format": "DD/MM/YYYY",  # moment date-time format
        "showClose": True,
        "showClear": True,
        "showTodayButton": True,
        "locale": "es"}


class SolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
        
        """ atrr class"""
        self.fields['ciudad'].widget.attrs['class'] = 'sel'

        """ atrr placeholder"""
        self.fields['fech_inicio'].widget.attrs['placeholder'] = 'Fecha de iniciación'
        self.fields['duracion_prevista'].widget.attrs['placeholder'] = 'Duración prevista'
        self.fields['ciudad'].widget.attrs['data-placeholder'] = 'Lugar de residencia durante la comisión'
        self.fields['gastos_previstos'].widget.attrs['placeholder'] = 'Gastos a solicitar'
        self.fields['motivo'].widget.attrs['placeholder'] = 'DETALLE DE LOS TRABAJOS REALIZADOS:'

    class Meta:
        model = Solicitud
        fields = ['fech_inicio','gastos_previstos', 'motivo','duracion_prevista', 'ciudad']
        widgets = {
            'fech_inicio': DatePickerInput(),
        }


class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo', 'patente']
