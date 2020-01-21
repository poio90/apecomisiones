from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Afiliado(models.Model):
    id_afiliado = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_afiliado = models.CharField(
        'Número de Afiliado', unique=True, max_length=45)
    num_tel = models.CharField(
        'Número de Telefono', max_length=11, blank=True, null=True)
    dni = models.CharField('DNI', unique=True,max_length=45, blank=True, null=True)

    class Meta:
        verbose_name = 'Afiliado'
        verbose_name_plural = 'Afiliados'
        managed = True
        db_table = 'afiliado'

    def __str__(self):
        return self.num_afiliado
