# Generated by Django 3.2.19 on 2023-11-21 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Asistencial', '0091_auto_20231121_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asigcupospac',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paciente'),
        ),
        migrations.AlterField(
            model_name='asigcupospac',
            name='parameCentroPuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.paramecentropuesto'),
        ),
    ]