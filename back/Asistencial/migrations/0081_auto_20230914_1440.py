# Generated by Django 3.2.19 on 2023-09-14 19:40

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Asistencial', '0080_auto_20230914_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='pacienteLocalizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=150)),
                ('referencia', models.CharField(max_length=150)),
                ('telefono', models.CharField(max_length=20)),
                ('telefonoAlterno', models.CharField(max_length=20)),
                ('latitud', models.CharField(blank=True, max_length=100, null=True)),
                ('longitud', models.CharField(blank=True, max_length=100, null=True)),
                ('cordePac', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, help_text='Point(longitude latitude)', null=True, srid=4326, verbose_name='Location in Map')),
                ('userReg', models.CharField(max_length=150)),
                ('fechaReg', models.DateField(auto_now_add=True)),
                ('cas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.cas')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paciente')),
                ('ubigeo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.ubigeo')),
            ],
        ),
    ]
