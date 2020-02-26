from django.db import models
from .models import Ciudad, Transporte

class Comision(models.Model):
    
    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_ciudad'
    )

    transporte = models.ForeignKey(
        'Transporte',
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_transporte'
    )

    fech_inicio = models.DateField()

    class Meta:
        abstract = True
        get_lates_by = 'fech_inicio'
        ordering = ['-fech_inicio']