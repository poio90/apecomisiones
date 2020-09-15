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
        "locale": "es"
        }


class SolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

        """ atrr class"""
        self.fields['ciudad'].widget.attrs['class'] = 'sel'
        self.fields['transporte'].widget.attrs['class'] = 'sel'

        """ atrr placeholder"""
        self.fields['fech_inicio'].widget.attrs['placeholder'] = 'Fecha de iniciación'
        self.fields['duracion_prevista'].widget.attrs['placeholder'] = 'Duración prevista'
        self.fields['ciudad'].widget.attrs['data-placeholder'] = 'Lugar de residencia durante la comisión'
        self.fields['transporte'].widget.attrs['data-placeholder'] = 'Unidad de legajo y Patente'
        self.fields['gastos_previstos'].widget.attrs['placeholder'] = 'Gastos a solicitar'
        self.fields['motivo'].widget.attrs['placeholder'] = 'DETALLE DE LOS TRABAJOS REALIZADOS:'

        """ atrr id"""
        self.fields['fech_inicio'].widget.attrs['id'] = 'date_inicio'

    class Meta:
        model = Solicitud
        fields = ['fech_inicio', 'gastos_previstos',
                  'motivo', 'duracion_prevista', 'ciudad','transporte']
        widgets = {
            'fech_inicio': DatePickerInput(),
        }


class RendicionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

        """ atrr class"""
        self.fields['ciudad'].widget.attrs['class'] = 'sel'
        self.fields['transporte'].widget.attrs['class'] = 'sel'

        """ atrr placeholder"""
        self.fields['fech_inicio'].widget.attrs['placeholder'] = 'Fecha de inicio'
        self.fields['fech_fin'].widget.attrs['placeholder'] = 'Fecha de finalización'
        self.fields['ciudad'].widget.attrs['data-placeholder'] = 'Lugar de residencia durante la comisión'
        self.fields['transporte'].widget.attrs['data-placeholder'] = 'Unidad de legajo y Patente'
        self.fields['gastos'].widget.attrs['placeholder'] = 'Gastos'

        """ atrr id"""
        self.fields['fech_inicio'].widget.attrs['id'] = 'date_inicio'
        self.fields['fech_fin'].widget.attrs['id'] = 'date_fin'

    class Meta:
        model = Anticipo
        fields = ['fech_inicio', 'fech_fin', 'gastos', 'ciudad','transporte']
        widgets = {
            'fech_inicio': DatePickerInput().start_of('event days'),
            'fech_fin': DatePickerInput().end_of('event days'),
        }


class DetalleTrabajoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
        
        """ atrr placeholder"""
        self.fields['km_salida'].widget.attrs['placeholder'] = 'Km de salida'
        self.fields['km_llegada'].widget.attrs['placeholder'] = 'Kn de llegada'
        self.fields['detalle_trabajo'].widget.attrs['placeholder'] = 'NOTA:'

    class Meta:
        model = DetalleTrabajo
        fields = ['km_salida', 'km_llegada', 'detalle_trabajo', ]


class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo', 'patente']
