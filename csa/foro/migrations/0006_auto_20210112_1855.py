# Generated by Django 3.1.4 on 2021-01-12 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foro', '0005_auto_20201231_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='lecturas',
            field=models.IntegerField(default=0, verbose_name='Lecturas'),
        ),
    ]
