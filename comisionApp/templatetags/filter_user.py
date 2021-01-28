import re
from django import template
from django.utils.safestring import mark_safe
from comisionApp.forms import CollectionUserForm
from comisionApp.models import Integrantes_x_Solicitud, Integrantes_x_Anticipo
from usuarios.models import User

register = template.Library()


@register.filter(name="num_af_solicitud")
def get_num_af_solicitud(value):
    if value != None:
        integrante = Integrantes_x_Solicitud.objects.values(
            'user').get(pk=value)
        user = User.objects.values('num_afiliado').get(pk=integrante['user'])
        data_input = '<input type="text" class="form-control" value="' + \
            user['num_afiliado'] + \
            '" placeholder="Número de afiliado a SEMPRE" readonly>'
    else:
        data_input = '<input type="text" class="form-control" placeholder="Número de afiliado a SEMPRE" readonly>'

    return mark_safe(data_input)


@register.filter(name="num_af_rendicion")
def get_num_af_rendicion(value):
    if value != None:
        integrante = Integrantes_x_Anticipo.objects.values(
            'user').get(pk=value)
        user = User.objects.values('num_afiliado').get(pk=integrante['user'])
        data_input = '<input type="text" class="form-control" value="' + \
            user['num_afiliado'] + \
            '" placeholder="Número de afiliado a SEMPRE" readonly>'
    else:
        data_input = '<input type="text" class="form-control" placeholder="Número de afiliado a SEMPRE" readonly>'

    return mark_safe(data_input)
