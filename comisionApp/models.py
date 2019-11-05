# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Agente(models.Model):
    id_agente = models.AutoField(primary_key=True)
    apellido = models.CharField(max_length=45)
    nombre = models.CharField(max_length=45)
    fecha_nacimiento = models.DateField()
    num_tel = models.CharField(max_length=11)
    email = models.CharField(max_length=45)
    dni = models.IntegerField()

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'
        ordering = ['apellido','nombre']
        managed = False
        db_table = 'agente'

    def __str__(self):
        return self.apellido


class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    ciudad = models.CharField(max_length=45)
    id_provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='id_provincia')

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['ciudad']
        managed = False
        db_table = 'ciudad'

    def __str__(self):
        return self.ciudad


class Comision(models.Model):
    id_comision = models.AutoField(primary_key=True)
    id_ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='id_ciudad')
    id_agente = models.ForeignKey(Agente, models.DO_NOTHING, db_column='id_agente')
    id_transporte = models.ForeignKey('Transporte', models.DO_NOTHING, db_column='id_transporte')
    fech_inicio = models.DateField()
    fech_fin = models.DateField()
    gasto = models.FloatField()

    class Meta:
        verbose_name = 'Comision'
        verbose_name_plural = 'Comisiones'
        managed = False
        db_table = 'comision'

    def __str__(self):
        return self.id_comision


class DetalleRecorrido(models.Model):
    id_det_recorrido = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora_salida = models.DateTimeField()
    hora_llegada = models.DateTimeField()
    salida = models.CharField(max_length=45)
    llegada = models.CharField(max_length=45)
    id_comision = models.ForeignKey(Comision, models.DO_NOTHING, db_column='id_comision')

    class Meta:
        managed = False
        db_table = 'detalle_recorrido'

    def __str__(self):
        return self.id_det_recorrido

class DetalleTrabajo(models.Model):
    id_det_trabajo = models.AutoField(primary_key=True)
    km_salida = models.IntegerField()
    km_llegada = models.IntegerField()
    detalle_trabajo = models.CharField(max_length=200)
    id_comision = models.ForeignKey(Comision, models.DO_NOTHING, db_column='id_comision')

    class Meta:
        managed = False
        db_table = 'detalle_trabajo'

    def __str__(self):
        return self.id_det_trabajo

class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    provincia = models.CharField(max_length=45)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        managed = False
        db_table = 'provincia'

    def __str__(self):
        return self.provincia

class Transporte(models.Model):
    id_transporte = models.AutoField(primary_key=True)
    num_legajo = models.CharField(max_length=45)
    patente = models.CharField(max_length=45)

    class Meta:
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'
        managed = False
        db_table = 'transporte'

    def __str__(self):
        return self.num_legajo