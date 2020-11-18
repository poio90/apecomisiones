from django.db import models
from comisionApp.models import Ciudad
from usuarios.models import User
from django.utils.translation import gettext_lazy as _


class ComprasServicios(models.Model):
    id_compras_servicios = models.AutoField(primary_key=True)

    localidad = models.ForeignKey(
        Ciudad,
        on_delete=models.SET_NULL,
        null=True,
    )

    motivo = models.TextField(_('Motivo del Requerimiento'))

    destino = models.CharField(
        _('Destino'), max_length=100, blank=True, null=True)

    # Requiriente
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    fecha_pedido = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _('Compras y Servicios')
        verbose_name_plural = _('Compras y Servicios')
        managed = True
        db_table = 'compras_servicios'

    def __str__(self):
        return '{}'.format(self.fecha_pedido)


class DetalleRequerido(models.Model):
    id_detalle = models.AutoField(primary_key=True)

    compras_servicios = models.ForeignKey(
        ComprasServicios,
        on_delete=models.CASCADE,
    )

    detalle_requerido = models.CharField(
        _('Detalle'), max_length=200, blank=True, null=True)

    monto = models.FloatField()

    class Meta:
        verbose_name = 'Detalle de lo requerido'
        managed = True
        db_table = 'detalle_requerido'
