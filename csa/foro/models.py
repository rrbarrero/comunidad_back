from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.loader import render_to_string, get_template
from ckeditor_uploader.fields import RichTextUploadingField
# from foro.tasks import send_async_mail


class TemaForo(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    imagen = models.ImageField(upload_to="public/static/uploads/%Y/%m/%d/")
    descripcion_corta = models.CharField(
        max_length=300, verbose_name="Descripción corta"
    )
    descripcion = models.CharField(max_length=300, verbose_name="Descripción")

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Temas de Hilos"


class PublicacionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(censurado=False)


class Publicacion(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Título")
    cuerpo = RichTextUploadingField(verbose_name="Cuerpo")
    autor = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    tema = models.ForeignKey(
        TemaForo,
        verbose_name="Tema",
        related_name="publicaciones",
        on_delete=models.CASCADE,
    )
    censurado = models.BooleanField(default=False, verbose_name="Censurar")
    lecturas = models.IntegerField(verbose_name="Lecturas", default=0)
    fecha_creacion = models.DateTimeField(editable=False)
    fecha_modificacion = models.DateTimeField()

    objects = PublicacionManager()
    all_objects = models.Manager()

    def __str__(self):
        return "{}".format(self.titulo)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.fecha_creacion = timezone.now()
        self.fecha_modificacion = timezone.now()
        return super(Publicacion, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Hilos"
        ordering = ["-fecha_creacion"]


class ComentarioPublicacionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(censurado=False)


class ComentarioPublicacion(models.Model):
    publicacion = models.ForeignKey(
        Publicacion,
        verbose_name="Publicación",
        related_name="comentarios",
        on_delete=models.CASCADE,
    )
    cuerpo = RichTextUploadingField(verbose_name="Cuerpo")
    autor = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(editable=False)
    fecha_modificacion = models.DateTimeField()
    censurado = models.BooleanField(default=False, verbose_name="Censurar")

    objects = ComentarioPublicacionManager()
    all_objects = models.Manager()

    def __str__(self):
        return "{}...".format(self.cuerpo[0:50])

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.fecha_creacion = timezone.now()
        self.fecha_modificacion = timezone.now()
        return super(ComentarioPublicacion, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Comentarios de hilos"
