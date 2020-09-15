from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
from .models import Licencia


class DatePickerInput(DatePickerInput):
    options = {
        "format": "DD/MM/YYYY",  # moment date-time format
        "showClose": True,
        "showClear": True,
        "showTodayButton": True,
        "locale": "es"}


class FormLicencia(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

        self.fields['dias_habiles_acum'].widget.attrs['autofocus'] = 'autofocus'

        """ atrr id"""
        self.fields['fecha_inicio'].widget.attrs['id'] = 'date_inicio'
        self.fields['fecha_fin'].widget.attrs['id'] = 'date_fin'
        self.fields['fecha_reintegro'].widget.attrs['id'] = 'date_reintegro'

        """ atrr class"""
        self.fields['ciudad'].widget.attrs['class'] = 'sel'

    class Meta:
        model = Licencia
        fields = ['dias_habiles_acum', 'dias_habiles_agregar',
                  'fecha_inicio', 'fecha_fin', 'fecha_reintegro', 'ciudad']
        widgets = {
            'fecha_inicio': DatePickerInput().start_of('event days'),
            'fecha_reintegro': DatePickerInput().end_of('event days'),
            'fecha_fin': DatePickerInput().end_of('event days'),
        }
