# Generated by Django 3.2.19 on 2023-09-14 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Asistencial', '0081_auto_20230914_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacientelocalizacion',
            name='latitud',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pacientelocalizacion',
            name='longitud',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pacientelocalizacion',
            name='referencia',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='pacientelocalizacion',
            name='telefonoAlterno',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
