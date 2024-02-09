# Generated by Django 3.1.1 on 2023-06-02 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Asistencial', '0063_auto_20230505_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='baseDatosProduccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.DateField()),
                ('serie', models.CharField(max_length=12)),
                ('servicio', models.CharField(max_length=20)),
                ('actividad', models.CharField(max_length=50)),
                ('subactividad', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('meta', models.IntegerField()),
            ],
        ),
    ]