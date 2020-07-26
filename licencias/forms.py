from django import forms
from django.core.exceptions import ValidationError
from .models import Licencia

class FormLicencia(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
        self.fields['fecha_inicio'].widget.attrs['id'] = 'date_inicio'
        self.fields['fecha_fin'].widget.attrs['id'] = 'date_fin'
        self.fields['fecha_reintegro'].widget.attrs['id'] = 'date_reintegro'
        self.fields['fecha_inicio'].widget.attrs['autocomplete'] = 'off'
        self.fields['fecha_fin'].widget.attrs['autocomplete'] = 'off'
        self.fields['fecha_reintegro'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Licencia
        fields = ['dias_habiles_acum','dias_habiles_agregar','fecha_inicio','fecha_fin','fecha_reintegro']