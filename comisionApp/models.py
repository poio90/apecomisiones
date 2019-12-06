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

class Agente(models.Model):
    id_agente = models.OneToOneField(User, on_delete=models.CASCADE)
    num_afiliado = models.CharField('Número de Afiliado',unique=True, max_length=45,primary_key=True)
    fecha_nacimiento = models.DateField()
    num_tel = models.CharField('Número de Telefono',max_length=11)
    dni = models.CharField('DNI',max_length=45)

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'
        managed = True
        db_table = 'agente'

    def __str__(self):
        return self.num_afiliado

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
    id_provincia = models.ForeignKey('Provincia',on_delete=models.CASCADE, db_column='id_provincia')

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
    num_legajo = models.CharField('Numero de Legajo',max_length=45)
    patente = models.CharField('Patente',max_length=45)

    class Meta:
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'
        managed = True
        db_table = 'transporte'

    def __str__(self):
        return self.num_legajo


class Comision(models.Model):
    id_comision = models.AutoField(primary_key=True)
    num_comision = models.CharField('Número de Comisión',unique=True,max_length=45)
    id_ciudad = models.ForeignKey(Ciudad,on_delete=models.SET_NULL,null=True, db_column='id_ciudad')
    num_afiliado = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, db_column='num_afiliado') 
    '''SET_NULL: establece la referencia en NULL (requiere que el campo sea anulable). Por ejemplo, 
    cuando elimina un usuario, es posible que desee conservar los comentarios que publicó en las 
    publicaciones de blog, pero digamos que fue publicado por un usuario anónimo (o eliminado). 
    Equivalente de SQL: SET NULL.'''
    id_transporte = models.ForeignKey('Transporte',on_delete=models.SET_NULL,null=True, db_column='id_transporte')
    fech_inicio = models.DateField()
    fech_fin = models.DateField()
    gasto = models.FloatField()
    motivo = RichTextField()
    duracion_prevista = models.CharField(max_length=45)

    class Meta:
        verbose_name = 'Comision'
        verbose_name_plural = 'Comisiones'
        managed = True
        db_table = 'comision'

    def __str__(self):
        return self.num_comision


class Itineraio(models.Model):
    id_itinerario = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora_salida = models.DateTimeField()
    hora_llegada = models.DateTimeField()
    salida = models.CharField(max_length=45)
    llegada = models.CharField(max_length=45)
    id_comision = models.ForeignKey(Comision, on_delete=models.DO_NOTHING, db_column='id_comision')

    class Meta:
        verbose_name = 'Itinerario'
        managed = True
        db_table = 'detalle_recorrido'

    def __str__(self):
        return self.id_det_recorrido

class DetalleTrabajo(models.Model):
    id_det_trabajo = models.AutoField(primary_key=True)
    km_salida = models.IntegerField()
    km_llegada = models.IntegerField()
    detalle_trabajo = RichTextField()
    id_comision = models.ForeignKey(Comision, on_delete=models.DO_NOTHING, db_column='id_comision')

    class Meta:
        managed = False
        db_table = 'detalle_trabajo'

    def __str__(self):
        return self.id_det_trabajo

'''https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Authentication'''