from django import forms
from django.core.exceptions import ValidationError
from .models import Licencia

class FormUpdateProfile(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = ['dias_habiles_acum','dias_habiles_agregar','fecha_inicio','fecha_fin','fecha_reintegro']