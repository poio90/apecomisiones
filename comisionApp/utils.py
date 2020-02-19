from django.db import models
from .models import Ciudad, Transporte

class Anticipo(models.Model):
    
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