# Generated by Django 3.1.4 on 2020-12-29 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20201217_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='frase_inspiradora',
            field=models.CharField(blank=True, max_length=200, verbose_name='Frase inspiradora'),
        ),
    ]
