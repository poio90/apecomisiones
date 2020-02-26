from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.


class User(AbstractUser):

    regex_num_af = RegexValidator(
        regex = r'(?:(\d{5})([/]\d{1})?)',
        message = "El número de afuliado debe ser ingresado en formato: 99999/9 o 99999. Hasta 7 caracteres son permitidos"
    )

    num_afiliado = models.CharField(
        'Número de Afiliado',
        validators = [regex_num_af],
        max_length =7,
        unique=True,
        error_messages = {
            'unique':'Ya existe un usuario con este número de afiliado'
        }
    )

    rexex_dni = RegexValidator(
        regex = r'^\d{8}(?:[-\s]\d{4})?$',
        message = "El DNI debe ser ingresado en formato: 09999999 o 99999999. Hasta 8 caracteres permitidos"
    )

    dni = models.CharField('DNI', unique=True,max_length=8, blank=True, null=True)

    regex_tel = RegexValidator(
        regex = r'^(?:\(?\d{2,3}\)?[- .]?\d{4,5}[- .]?\(?\d{4}\)?)',
        message = "El número de telefono debe ser ingresado sin 0 y 15. Hasta 10 digitos permitidos"
    )

    num_tel = models.CharField(
        'Número de Telefono',
        validators = [regex_tel],
        max_length=10,
        blank=True,
    )

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELD = ['username', 'num_afiliado', 'last_name', 'first_name']

    class Meta:
        verbose_name = 'Afiliado'
        verbose_name_plural = 'Afiliados'

    def __str__(self):
        return '{} {} {}'.format(self.num_afiliado,self.last_name,self.first_name)
