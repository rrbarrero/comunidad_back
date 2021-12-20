from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Plantilla(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre", unique=True)
    identificador = models.SlugField(max_length=255, unique=True)
    asunto = models.CharField(max_length=255, verbose_name="Asunto")
    body_content = RichTextUploadingField(verbose_name="Contenido")

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.identificador = slugify(self.nombre)
        super(Plantilla, self).save(*args, **kwargs)
