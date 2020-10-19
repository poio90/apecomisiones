from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    regex_num_af = RegexValidator(
        regex=r'(?:(\d{5})([/]\d{1})?)',
        message="El número de afiliado debe ser ingresado en formato: 99999/9 o 99999. Hasta 7 caracteres son permitidos"
    )

    num_afiliado = models.CharField(
        'Número de Afiliado',
        validators=[regex_num_af],
        max_length=7,
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este número de afiliado'
        }
    )

    regex_dni = RegexValidator(
        regex=r'^\d{8}(?:[-\s]\d{4})?$',
        message="El DNI debe ser ingresado en formato: 09999999 o 99999999. Hasta 8 caracteres permitidos"
    )

    dni = models.CharField(
        'DNI',
        unique=True,
        max_length=8,
        validators=[regex_dni, MinLengthValidator(7)],
        null=True,
        help_text=_(
            'El DNI debe ser ingresado en formato: 09999999 o 99999999. Hasta 8 caracteres permitidos'
        ),
    )

    regex_tel = RegexValidator(
        regex=r'^(?:\(?\d{2,3}\)?[- .]?\d{4,5}[- .]?\(?\d{4}\)?)',
        message="El número de telefono debe ser ingresado sin 0 y 15, no se permiten letras. Hasta 10 digitos permitidos"
    )

    num_tel = models.CharField(
        'Número de Telefono',
        validators=[regex_tel, MinLengthValidator(10)],
        max_length=10,
        blank=True,
        help_text=_(
            'El número de telefono debe ser ingresado sin 0 y 15, no se permiten letras. Hasta 10 digitos permitidos'
        ),
    )

    CATEGORIAS_CHOICE = (
        ('A', '6'),
        ('B', '7'),
        ('C', '8'),
        ('D', '9'),
        ('E', '10'),
        ('F', '11'),
        ('G', '12'),
        ('H', '13'),
        ('I', '14'),
        ('J', '15'),
        ('K', '16'),
        ('L', '17'),
        ('M', '18'),
    )

    categoria = models.CharField(
        _('categoría'),
        choices=CATEGORIAS_CHOICE,
        max_length=2,
        help_text=_(
            'Indica la categoría del afiliado'
        ),
        blank=True,
    )

    reemplazo = models.BooleanField(
        _('reemplazo'),
        default=False,
        help_text=_(
            'Indica si el usuario esta en reeplazo de categoría'
        ),
        blank=True,
    )

    categoria_reemplazo = models.CharField(
        _('categoría'),
        choices=CATEGORIAS_CHOICE,
        max_length=2,
        help_text=_(
            'Indica la categoría que está reemplazando el afiliado'
        ),
        blank=True,
    )

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['username', 'email',
                       'num_afiliado', 'last_name', 'first_name']

    class Meta:
        verbose_name = 'Afiliado'
        verbose_name_plural = 'Afiliados'

    def __str__(self):
        return '{} {}'.format(
            self.last_name,
            self.first_name,
        )
