# Generated by Django 3.1.1 on 2023-01-05 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Asistencial', '0043_auto_20230105_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutricion',
            name='albSerica',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='circuBra',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='diagNutricional',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='frecuencia',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='imc',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='ingestaCalorica',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='ingestaCaloricaT',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='ingestaProteica',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='ingestaProteicaT',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='interveNutricional',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='peso',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='porcentajeCMB',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='talla',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='tipoPaciente',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='turno',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
