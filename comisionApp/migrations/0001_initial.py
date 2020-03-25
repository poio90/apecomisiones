# Generated by Django 2.2.6 on 2020-03-25 16:48

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anticipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fech_inicio', models.DateField()),
                ('num_comision', models.CharField(max_length=45, unique=True, verbose_name='Número de Comisión')),
                ('fech_fin', models.DateField()),
                ('gastos', models.FloatField()),
            ],
            options={
                'verbose_name': 'Anticipo',
                'verbose_name_plural': 'Anticipos',
                'db_table': 'anticipo_comision',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id_ciudad', models.AutoField(primary_key=True, serialize=False)),
                ('ciudad', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name': 'Ciudad',
                'verbose_name_plural': 'Ciudades',
                'db_table': 'ciudad',
                'ordering': ['ciudad'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DetalleTrabajo',
            fields=[
                ('id_det_trabajo', models.AutoField(primary_key=True, serialize=False)),
                ('km_salida', models.IntegerField()),
                ('km_llegada', models.IntegerField()),
                ('detalle_trabajo', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Detalle de Trabajo',
                'db_table': 'detalle_trabajo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Integrantes_x_Anticipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_de_registro', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Integrantes de anticipo',
                'verbose_name_plural': 'Integrantes por anticipo',
                'db_table': 'integrantes_x_anticipo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id_provincia', models.AutoField(primary_key=True, serialize=False)),
                ('provincia', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
                'db_table': 'provincia',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Transporte',
            fields=[
                ('id_transporte', models.AutoField(primary_key=True, serialize=False)),
                ('num_legajo', models.CharField(max_length=45, unique=True, verbose_name='Numero de Legajo')),
                ('patente', models.CharField(max_length=45, verbose_name='Patente')),
            ],
            options={
                'verbose_name': 'Transporte',
                'verbose_name_plural': 'Transportes',
                'db_table': 'transporte',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ubicaciones',
            fields=[
                ('id_ubicacion', models.AutoField(primary_key=True, serialize=False)),
                ('ubicacion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Ubicacion',
                'verbose_name_plural': 'Ubicaciones',
                'db_table': 'ubicacion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fech_inicio', models.DateField()),
                ('fecha_pedido', models.DateField(auto_now_add=True)),
                ('gastos_previstos', models.FloatField()),
                ('motivo', ckeditor.fields.RichTextField()),
                ('duracion_prevista', models.CharField(max_length=20)),
                ('ciudad', models.ForeignKey(db_column='id_ciudad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='comisionApp.Ciudad')),
                ('transporte', models.ForeignKey(db_column='id_transporte', null=True, on_delete=django.db.models.deletion.SET_NULL, to='comisionApp.Transporte')),
            ],
            options={
                'verbose_name': 'Solicitud de Comisón',
                'verbose_name_plural': 'Solicitudes',
                'db_table': 'solicitud_comision',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Itineraio',
            fields=[
                ('id_itinerario', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('hora_salida', models.DateTimeField()),
                ('hora_llegada', models.DateTimeField()),
                ('salida', models.CharField(max_length=45)),
                ('llegada', models.CharField(max_length=45)),
                ('rendicion', models.ForeignKey(db_column='id_anticipo', on_delete=django.db.models.deletion.DO_NOTHING, to='comisionApp.Anticipo')),
            ],
            options={
                'verbose_name': 'Itinerario',
                'db_table': 'itinerario',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Integrantes_x_Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_de_registro', models.DateField(auto_now_add=True)),
                ('solicitud', models.ForeignKey(db_column='id_solicitud', null=True, on_delete=django.db.models.deletion.SET_NULL, to='comisionApp.Solicitud')),
            ],
            options={
                'verbose_name': 'Integrantes de solicitud',
                'verbose_name_plural': 'Integrantes por solicitudes',
                'db_table': 'integrantes_x_solicitud',
                'managed': True,
            },
        ),
    ]
