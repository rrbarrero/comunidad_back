# Generated by Django 3.1.4 on 2020-12-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201217_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='entradilla',
            field=models.CharField(max_length=350, verbose_name='Entradilla'),
        ),
    ]