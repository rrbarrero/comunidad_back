# Generated by Django 3.1.6 on 2021-02-15 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20210212_2317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articulo',
            options={'ordering': ['-fecha_creacion'], 'verbose_name_plural': 'Articulos'},
        ),
    ]
