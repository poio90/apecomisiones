# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    provincia = models.CharField(max_length=45)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        managed = True
        db_table = 'provincia'

    def __str__(self):
        return self.provincia


class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    ciudad = models.CharField(max_length=45)
    id_provincia = models.ForeignKey(
        'Provincia', on_delete=models.CASCADE, db_column='id_provincia')

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['ciudad']
        managed = True
        db_table = 'ciudad'

    def __str__(self):
        return self.ciudad


class Transporte(models.Model):
    id_transporte = models.AutoField(primary_key=True)
    num_legajo = models.CharField(
        'Numero de Legajo', unique=True, max_length=45)
    patente = models.CharField('Patente', max_length=45)

    class Meta:
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'
        managed = True
        db_table = 'transporte'

    def __str__(self):
        return self.num_legajo


class Ubicaciones(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Ubicacion'
        verbose_name_plural = 'Ubicaciones'
        managed = True
        db_table = 'ubicacion'

    def __str__(self):
        return self.ubicacion

class Solicitud_Comision(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField(auto_now_add=True)
    id_ciudad = models.ForeignKey(
        Ciudad, on_delete=models.SET_NULL, null=True, db_column='id_ciudad')
    id_transporte = models.ForeignKey(
        'Transporte', on_delete=models.SET_NULL, null=True, db_column='id_transporte')
    fech_inicio = models.DateField()
    gastos_previsto = models.FloatField()
    motivo = RichTextField()
    duracion_prevista = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Solicitud de Comisón'
        verbose_name_plural = 'Solicitudes de Comisiones'
        managed = True
        db_table = 'solicitud_comision'

    def __str__(self):
        return '{}'.format(self.fecha_pedido)


class Comision(models.Model):
    id_comision = models.AutoField(primary_key=True)
    num_comision = models.CharField(
        'Número de Comisión', unique=True, max_length=45)
    id_ciudad = models.ForeignKey(
        Ciudad, on_delete=models.SET_NULL, null=True, db_column='id_ciudad')
    id_transporte = models.ForeignKey(
        'Transporte', on_delete=models.SET_NULL, null=True, db_column='id_transporte')
    fech_inicio = models.DateField()
    fech_fin = models.DateField()
    gastos = models.FloatField()

    class Meta:
        verbose_name = 'Comision'
        verbose_name_plural = 'Comisiones'
        managed = True
        db_table = 'comision'

    def __str__(self):
        return self.num_comision


'''SET_NULL: establece la referencia en NULL (requiere que el campo sea anulable). Por ejemplo, 
    cuando elimina un usuario, es posible que desee conservar los comentarios que publicó en las 
    publicaciones de blog, pero digamos que fue publicado por un usuario anónimo (o eliminado). 
    Equivalente de SQL: SET NULL.'''


class Comision_x_Afiliado(models.Model):
    id_comision = models.ForeignKey(
        Comision, on_delete=models.SET_NULL, null=True, db_column='id_comision')
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id_afiliado = models.ForeignKey('usuarios.Afiliado', on_delete=models.SET_NULL, null=True)
    fecha_de_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comision por Afiliado'
        verbose_name_plural = 'Comisiones por Afiliados'
        unique_together = (('id_user','id_comision'),)
        managed = True
        db_table = 'comision_x_afiliado'
    
    def __str__(self):
        return '{} {} {}'.format(self.id_comision,self.id_user.username,self.id_afiliado.num_afiliado)


class Solicitud_x_Afiliado(models.Model):
    id_solicitud = models.ForeignKey(
        Comision, on_delete=models.SET_NULL, null=True, db_column='id_solicitud')
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_de_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Solicitud por Afiliado'
        verbose_name_plural = 'Solicitudes por Afiliados'
        managed = True
        db_table = 'solicitud_x_afiliado'


class Itineraio(models.Model):
    id_itinerario = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora_salida = models.DateTimeField()
    hora_llegada = models.DateTimeField()
    salida = models.CharField(max_length=45)
    llegada = models.CharField(max_length=45)
    id_comision = models.ForeignKey(
        Comision, on_delete=models.DO_NOTHING, db_column='id_comision')

    class Meta:
        verbose_name = 'Itinerario'
        managed = True
        db_table = 'itinerario'

    def __str__(self):
        return self.id_det_recorrido


class DetalleTrabajo(models.Model):
    id_det_trabajo = models.AutoField(primary_key=True)
    km_salida = models.IntegerField()
    km_llegada = models.IntegerField()
    detalle_trabajo = RichTextField()
    id_comision = models.ForeignKey(
        Comision, on_delete=models.DO_NOTHING, db_column='id_comision')

    class Meta:
        managed = False
        db_table = 'detalle_trabajo'

    def __str__(self):
        return '{}'.format(self.id_det_trabajo)


''' https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Authentication
    https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    https://www.youtube.com/watch?v=TWYPq_AGVjQ'''
