# Generated by Django 2.2.6 on 2019-12-11 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agente',
            name='dni',
            field=models.CharField(blank=True, max_length=45, null=True, verbose_name='DNI'),
        ),
        migrations.AlterField(
            model_name='agente',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='agente',
            name='num_tel',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Número de Telefono'),
        ),
    ]
