from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
from .models import *
from usuarios.models import User
from django.forms.models import BaseInlineFormSet


class DatePickerInput(DatePickerInput):
    options = {
        "format": "DD/MM/YYYY",  # moment date-time format
        "showClose": True,
        "showClear": True,
        "showTodayButton": True,
        "locale": "es"
    }

class TimeInput(forms.TimeInput):
    input_type = "time"



class SolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

        """ atrr class"""
        self.fields['ciudad'].widget.attrs['class'] = 'sel'
        self.fields['transporte'].widget.attrs['class'] = 'sel'

        """ atrr placeholder"""
        self.fields['fecha_inicio'].widget.attrs['placeholder'] = 'Fecha de iniciación'
        self.fields['duracion_prevista'].widget.attrs['placeholder'] = 'Duración prevista'
        self.fields['ciudad'].widget.attrs['data-placeholder'] = 'Lugar de residencia durante la comisión'
        self.fields['ciudad'].label = 'Lugar de residencia durante la comisión'
        self.fields['transporte'].widget.attrs['data-placeholder'] = 'Unidad de legajo y Patente'
        self.fields['gastos_previstos'].widget.attrs['placeholder'] = 'Gastos a solicitar'
        self.fields['motivo'].widget.attrs['placeholder'] = 'DETALLE DE LOS TRABAJOS REALIZADOS:'

        """ atrr id"""
        self.fields['fecha_inicio'].widget.attrs['id'] = 'date_inicio'

    class Meta:
        model = Solicitud
        fields = ['fecha_inicio', 'gastos_previstos',
                  'motivo', 'duracion_prevista', 'ciudad', 'transporte']
        widgets = {
            'fecha_inicio': DatePickerInput(),
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
        self.fields['fecha_inicio'].widget.attrs['placeholder'] = 'Fecha de inicio'
        self.fields['fecha_fin'].widget.attrs['placeholder'] = 'Fecha de finalización'
        self.fields['ciudad'].widget.attrs['data-placeholder'] = 'Lugar de residencia durante la comisión'
        self.fields['ciudad'].label = 'Lugar de residencia durante la comisión'
        self.fields['transporte'].widget.attrs['data-placeholder'] = 'Unidad de legajo y Patente'
        self.fields['gastos'].widget.attrs['placeholder'] = 'Gastos'

        """ atrr id"""
        self.fields['fecha_inicio'].widget.attrs['id'] = 'date_inicio'
        self.fields['fecha_fin'].widget.attrs['id'] = 'date_fin'

    class Meta:
        model = Anticipo
        fields = ['fecha_inicio', 'fecha_fin',
                  'gastos', 'ciudad', 'transporte']
        widgets = {
            'fecha_inicio': DatePickerInput().start_of('event days'),
            'fecha_fin': DatePickerInput().end_of('event days'),
        }

class ItinerarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItinerarioForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
        
    
    class Meta:
        model = Itinerario
        fields = '__all__'
        widgets = {
            'hora_salida': TimeInput(),
            'hora_llegada': TimeInput(),
        }


class DetalleTrabajoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetalleTrabajoForm, self).__init__(*args, **kwargs)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Transporte
        fields = ['num_legajo', 'patente']


class CollectionUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CollectionUserForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
            self.fields[myField].label = ''

        self.fields['user'].queryset = User.objects.all().order_by('last_name').filter(is_active=1)
        self.fields['user'].widget.attrs['class'] = 'sel'
        self.fields['user'].widget.attrs['data-placeholder'] = 'Apellido y Nombre'
        self.fields['user'].widget.attrs['required'] = 'true'

    class Meta:
        model = Integrantes_x_Solicitud
        fields = ['user']


SolicitudFormSet = inlineformset_factory(Solicitud, Integrantes_x_Solicitud,
                                              form=CollectionUserForm, can_delete=True, extra=1)

RendicionFormSet = inlineformset_factory(Anticipo, Integrantes_x_Anticipo,
                                              form=CollectionUserForm, can_delete=True, extra=1)

ItinerarioFormSet = inlineformset_factory(Anticipo, Itinerario,
                                              form=ItinerarioForm, can_delete=True, extra=1)