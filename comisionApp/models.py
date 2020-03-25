from django.db import models
from django.conf import settings
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
        'Provincia',
        on_delete=models.CASCADE,
        db_column='id_provincia'
    )

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
        'Numero de Legajo',
        unique=True,
        max_length=45
    )

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


class Solicitud(models.Model):
    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_ciudad'
    )

    transporte = models.ForeignKey(
        Transporte,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_transporte'
    )

    fech_inicio = models.DateField()

    fecha_pedido = models.DateField(auto_now_add=True)
    gastos_previstos = models.FloatField()
    motivo = RichTextField()
    duracion_prevista = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Solicitud de Comisón'
        verbose_name_plural = 'Solicitudes'
        managed = True
        db_table = 'solicitud_comision'

    def __str__(self):
        return '{}'.format(self.fecha_pedido)


class Anticipo(models.Model):
    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_ciudad'
    )

    transporte = models.ForeignKey(
        Transporte,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_transporte'
    )

    fech_inicio = models.DateField()

    num_comision = models.CharField(
        'Número de Comisión',
        unique=True,
        max_length=45
    )

    fech_fin = models.DateField()
    gastos = models.FloatField()

    class Meta:
        verbose_name = 'Anticipo'
        verbose_name_plural = 'Anticipos'
        managed = True
        db_table = 'anticipo_comision'

    def __str__(self):
        return '{} {} {}'.format(self.fech_inicio, self.num_comision,self.ciudad.ciudad)


''' SET_NULL: establece la referencia en NULL (requiere que el campo sea anulable). Por ejemplo, 
    cuando elimina un usuario, es posible que desee conservar los comentarios que publicó en las 
    publicaciones de blog, pero digamos que fue publicado por un usuario anónimo (o eliminado). 
    Equivalente de SQL: SET NULL.'''


class Integrantes_x_Solicitud(models.Model):
    solicitud = models.ForeignKey(
        Solicitud,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_solicitud'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_user'
    )

    fecha_de_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Integrantes de solicitud'
        verbose_name_plural = 'Integrantes por solicitudes'
        unique_together = (('user', 'solicitud'),)
        managed = True
        db_table = 'integrantes_x_solicitud'

    def __str__(self):
        return '{} {} {}'.format(self.solicitud, self.user.username, self.user.num_afiliado)


class Integrantes_x_Anticipo(models.Model):

    anticipo = models.ForeignKey(
        Anticipo,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_anticipo'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_user'
    )

    fecha_de_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Integrantes de anticipo'
        verbose_name_plural = 'Integrantes por anticipo'
        unique_together = (('user', 'anticipo'),)
        managed = True
        db_table = 'integrantes_x_anticipo'

    def __str__(self):
        return '{} {} {}'.format(self.anticipo, self.user, self.user.num_afiliado)


class Itineraio(models.Model):
    id_itinerario = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora_salida = models.DateTimeField()
    hora_llegada = models.DateTimeField()
    salida = models.CharField(max_length=45)
    llegada = models.CharField(max_length=45)
    rendicion = models.ForeignKey(
        Anticipo,
        on_delete=models.DO_NOTHING,
        db_column='id_anticipo'
    )

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

    rendicion = models.ForeignKey(
        Anticipo,
        on_delete=models.DO_NOTHING,
        db_column='id_anticipo'
    )

    class Meta:
        verbose_name = 'Detalle de Trabajo'
        managed = True
        db_table = 'detalle_trabajo'

    def __str__(self):
        return '{}'.format(self.id_det_trabajo)


''' https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Authentication
    https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    https://www.youtube.com/watch?v=TWYPq_AGVjQ
    
    select anticipo_comision.num_comision,ciudad.ciudad from anticipo_comisionn JOIN ciudad ON anticipo_comision.id_ciudad=ciudad.id_ciudad IS IN (SELECT * FROM integrantes_x_anticipo WHERE integrantes_x_anticipo.id_user=1) GROUP BY 
    select anticipo_comision.num_comision,ciudad.ciudad,integrantes_x_anticipo.fecha_de_registro from integrantes_x_anticipo,anticipo_comisionn,ciudad,usuarios_user where integrantes_x_anticipo.id_user=usuarios_user.id and integrantes_x_anticipo.id_anticipo=anticipo_comision.id and anticipo_comision.id_ciudad=ciudad.id_ciudad
    
    select anticipo_comision.num_comision,ciudad.ciudad from anticipo_comisionn JOIN ciudad ON anticipo_comision.id_ciudad=ciudad.id_ciudad WHERE anticipo_comision.num_comision='12345'
    
    SELECT anticipo_comision.fech_inicio, anticipo_comision.num_comision, ciudad.ciudad FROM anticipo_comision 
    JOIN ciudad on anticipo_comision.id_ciudad=ciudad.id_ciudad 
    WHERE anticipo_comision.id IN (SELECT integrantes_x_anticipo.id_anticipo FROM integrantes_x_anticipo WHERE integrantes_x_anticipo.id_user=1) 
    GROUP BY anticipo_comision.fech_inicio, anticipo_comision.num_comision, ciudad.ciudad'''
