# Generated by Django 3.1.1 on 2023-04-03 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Asistencial', '0060_auto_20230331_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='cas',
            name='estado',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
