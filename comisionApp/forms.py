from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
from .models import *


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

    class Meta:
        model = Solicitud
        fields = ['fech_inicio', ]
        widgets = {
            'fech_inicio': DatePickerInput(),
        }


class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ['num_legajo', 'patente']
