from django.db import models
from django.forms import model_to_dict
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
    
    def toJSON(self):
        return model_to_dict(self)

    def __str__(self):
        return '{} {}'.format(self.num_legajo,self.patente)


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
    )

    transporte = models.ForeignKey(
        Transporte,
        on_delete=models.SET_NULL,
        null=True,
    )

    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='usersolicitud',
        through='Integrantes_x_Solicitud'
    )

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='creadopor',
        blank=True,
        null=True,
    )

    fecha_inicio = models.DateField()
    fecha_pedido = models.DateField(auto_now_add=True)
    gastos_previstos = models.FloatField()
    motivo = models.TextField()
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

    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='userrendicion',
        through='Integrantes_x_Anticipo'
    )

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    gastos = models.FloatField()

    class Meta:
        verbose_name = 'Anticipo'
        verbose_name_plural = 'Anticipos'
        managed = True
        db_table = 'anticipo_comision'

    def __str__(self):
        return '{} {} {} {} {} {}'.format(
            self.fecha_inicio,
            self.ciudad.ciudad,
            self.fecha_fin,
            self.gastos,
            self.transporte.num_legajo,
            self.transporte.patente)


''' SET_NULL: establece la referencia en NULL (requiere que el campo sea anulable). Por ejemplo, 
    cuando elimina un usuario, es posible que desee conservar los comentarios que publicó en las 
    publicaciones de blog, pero digamos que fue publicado por un usuario anónimo (o eliminado). 
    Equivalente de SQL: SET NULL.'''


class Integrantes_x_Solicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud,on_delete=models.CASCADE,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,)

    fecha_de_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Integrantes de solicitud'
        verbose_name_plural = 'Integrantes por solicitudes'
        unique_together = (('user', 'solicitud'),)
        managed = True
        db_table = 'integrantes_x_solicitud'

    def __str__(self):
        return '{} {}'.format(self.solicitud, self.user)


class Integrantes_x_Anticipo(models.Model):

    anticipo = models.ForeignKey(Anticipo,on_delete=models.CASCADE,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,)

    fecha_de_registro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Integrantes de anticipo'
        verbose_name_plural = 'Integrantes por anticipo'
        unique_together = (('user', 'anticipo'),)
        managed = True
        db_table = 'integrantes_x_anticipo'

    def __str__(self):
        return '{} {}'.format(self.anticipo,self.user)


class Itineraio(models.Model):
    id_itinerario = models.AutoField(primary_key=True)
    nombre_afiliado = models.CharField(max_length=150)
    dia = models.CharField(max_length=10)
    mes = models.CharField(max_length=10)
    hora_salida = models.CharField(max_length=6)
    hora_llegada = models.CharField(max_length=6)
    salida = models.CharField(max_length=45)
    llegada = models.CharField(max_length=45)

    anticipo = models.ForeignKey(
        Anticipo,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Itinerario'
        managed = True
        db_table = 'itinerario'

    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(
            self.nombre_afiliado,
            self.dia,
            self.mes,
            self.hora_salida,
            self.hora_llegada,
            self.salida,
            self.llegada)


class DetalleTrabajo(models.Model):
    id_det_trabajo = models.AutoField(primary_key=True)
    km_salida = models.IntegerField(blank=True,null=True)
    km_llegada = models.IntegerField(blank=True,null=True)
    detalle_trabajo = models.TextField()

    anticipo = models.OneToOneField(
        Anticipo,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Detalle de Trabajo'
        managed = True
        db_table = 'detalle_trabajo'

    def __str__(self):
        return '{} {} {}'.format(
            self.km_salida,
            self.km_llegada,
            self.detalle_trabajo
            )


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
