from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Licencia(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_user'
    )

    dias_habiles_acum = models.IntegerField()
    dias_habiles_agregar = models.IntegerField()
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_reintegro = models.DateField()