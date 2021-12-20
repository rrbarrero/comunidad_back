# Generated by Django 3.1.4 on 2020-12-31 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foro', '0003_temaforo_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentariopublicacion',
            name='publicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='foro.publicacion', verbose_name='Publicación'),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicaciones', to='foro.temaforo', verbose_name='Tema'),
        ),
    ]
