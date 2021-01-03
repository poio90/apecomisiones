from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from .models import ComprasServicios, DetalleRequerido
from usuarios.models import User


class ComprasServiciosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ComprasServiciosForm, self).__init__(*args, **kwargs)

        self.fields['localidad'].widget.attrs['class'] = 'sel'
        self.fields['localidad'].widget.attrs['data-placeholder'] = 'Localidad'

        self.fields['transporte'].widget.attrs['class'] = 'sel'
        self.fields['transporte'].widget.attrs['data-placeholder'] = 'Unidad de legajo y Patente'

    class Meta:
        model = ComprasServicios
        fields = ['motivo', 'destino', 'localidad','vehículo','rep_vehículo','transporte']
        widget = {
            'vehículo': forms.ChoiceField(
                widget=forms.CheckboxSelectMultiple,
            )
        }


class DetalleRequeridoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetalleRequeridoForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
        
        self.fields['detalle_requerido'].widget.attrs['placeholder'] = 'Detalle de lo requerido'
        self.fields['monto'].widget.attrs['placeholder'] = 'Monto'

    class Meta:
        model = DetalleRequerido
        fields = '__all__'


DetalleRequeridoFormSet = inlineformset_factory(ComprasServicios, DetalleRequerido,
                                                form=DetalleRequeridoForm, can_delete=True, extra=1)
