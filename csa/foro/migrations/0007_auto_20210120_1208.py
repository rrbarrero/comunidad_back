# Generated by Django 3.1.5 on 2021-01-20 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foro', '0006_auto_20210112_1855'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comentariopublicacion',
            options={'verbose_name_plural': 'Comentarios de hilos'},
        ),
        migrations.AlterModelOptions(
            name='publicacion',
            options={'verbose_name_plural': 'Hilos'},
        ),
        migrations.AlterModelOptions(
            name='temaforo',
            options={'verbose_name_plural': 'Temas de Hilos'},
        ),
    ]
