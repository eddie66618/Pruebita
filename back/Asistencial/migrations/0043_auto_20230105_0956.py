# Generated by Django 3.1.1 on 2023-01-05 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Asistencial', '0042_auto_20221230_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutricion',
            name='ValGlobalSub',
            field=models.CharField(blank=True, default='NA', max_length=30, null=True),
        ),
    ]
