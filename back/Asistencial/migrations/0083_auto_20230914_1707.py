# Generated by Django 3.2.19 on 2023-09-14 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Asistencial', '0082_auto_20230914_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacientelocalizacion',
            name='cas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asistencial.cas', unique=True),
        ),
    ]