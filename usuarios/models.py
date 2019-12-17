from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Afiliado(User):
    num_afiliado = models.CharField('Número de Afiliado',unique=True, max_length=45)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    num_tel = models.CharField('Número de Telefono',max_length=11,blank=True, null=True)
    dni = models.CharField('DNI',max_length=45,blank=True, null=True)

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'
        managed = True
        db_table = 'afiliado'

    def __str__(self):
        return self.num_afiliado
