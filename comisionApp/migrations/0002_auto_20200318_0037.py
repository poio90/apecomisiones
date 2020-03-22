# Generated by Django 2.2.6 on 2020-03-18 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comisionApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='integrantes_x_solicitud',
            name='user',
            field=models.ForeignKey(db_column='id_user', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='integrantes_x_anticipo',
            name='rendicion',
            field=models.ForeignKey(db_column='id_anticipo', null=True, on_delete=django.db.models.deletion.SET_NULL, to='comisionApp.Anticipo'),
        ),
        migrations.AddField(
            model_name='integrantes_x_anticipo',
            name='user',
            field=models.ForeignKey(db_column='id_user', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detalletrabajo',
            name='rendicion',
            field=models.ForeignKey(db_column='id_anticipo', on_delete=django.db.models.deletion.DO_NOTHING, to='comisionApp.Anticipo'),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='id_provincia',
            field=models.ForeignKey(db_column='id_provincia', on_delete=django.db.models.deletion.CASCADE, to='comisionApp.Provincia'),
        ),
        migrations.AddField(
            model_name='anticipo',
            name='ciudad',
            field=models.ForeignKey(db_column='id_ciudad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='comisionApp.Ciudad'),
        ),
        migrations.AddField(
            model_name='anticipo',
            name='transporte',
            field=models.ForeignKey(db_column='id_transporte', null=True, on_delete=django.db.models.deletion.SET_NULL, to='comisionApp.Transporte'),
        ),
        migrations.AlterUniqueTogether(
            name='integrantes_x_solicitud',
            unique_together={('user', 'solicitud')},
        ),
        migrations.AlterUniqueTogether(
            name='integrantes_x_anticipo',
            unique_together={('user', 'rendicion')},
        ),
    ]
