# Generated by Django 3.1.4 on 2020-12-17 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='perfil', serialize=False, to='auth.user')),
                ('ocupacion', models.CharField(blank=True, max_length=300, verbose_name='Ocupación')),
                ('mail_confirmado', models.BooleanField(default=False, verbose_name='Mail confirmado')),
            ],
        ),
    ]
