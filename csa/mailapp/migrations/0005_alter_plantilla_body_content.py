# Generated by Django 3.2.9 on 2021-11-08 12:20

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailapp', '0004_plantilla_identificador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantilla',
            name='body_content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Contenido'),
        ),
    ]