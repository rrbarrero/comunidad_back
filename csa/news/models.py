from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class NoticiaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publico=True)


class Noticia(models.Model):

    PRIMERO = "1"
    SEGUNDO = "2"
    TERCERO = "3"

    POSITION_OPTIONS = (
        (PRIMERO, "Posición 1, principal"),
        (SEGUNDO, "Posición 2, abajo izquierda"),
        (TERCERO, "Posición 3, abajo derecha"),
    )

    titulo = models.CharField(max_length=150, verbose_name="Título")
    posicion = models.CharField(
        max_length=1,
        choices=POSITION_OPTIONS,
        default=PRIMERO,
    )
    imagen = models.ImageField(upload_to="public/static/uploads/%Y/%m/%d/")
    entradilla = models.CharField(max_length=350, verbose_name="Entradilla")
    cuerpo = RichTextUploadingField(verbose_name="Cuerpo")
    publico = models.BooleanField(default=False, verbose_name="Publicar")
    autor = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(editable=False)
    fecha_modificacion = models.DateTimeField()

    objects = NoticiaManager()
    all_objects = models.Manager()

    def __str__(self):
        return "{}".format(self.titulo)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.fecha_creacion = timezone.now()
        self.fecha_modificacion = timezone.now()
        return super(Noticia, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Noticias"
        ordering = ["-fecha_creacion"]


class ComentarioNoticiaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(censurado=False)


class ComentarioNoticia(models.Model):
    noticia = models.ForeignKey(
        Noticia,
        related_name="comentarios",
        verbose_name="Noticia",
        on_delete=models.CASCADE,
    )
    cuerpo = RichTextUploadingField(verbose_name="Cuerpo")
    autor = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(editable=False)
    fecha_modificacion = models.DateTimeField()
    censurado = models.BooleanField(default=False, verbose_name="Censurar")

    objects = ComentarioNoticiaManager()
    all_objects = models.Manager()

    def __str__(self):
        return "{}...".format(self.cuerpo[0:50])

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.fecha_creacion = timezone.now()
        self.fecha_modificacion = timezone.now()
        return super(ComentarioNoticia, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Comentarios"
        ordering = ["fecha_creacion"]