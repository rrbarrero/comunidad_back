from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string, get_template
from csa.celery import app as celery_app
from django.core.mail import send_mail


# No es posible meterlo en tasks por dependencia cíclica
@celery_app.task
def notify_new_article(articulo_id, autor_id):
    """Envía un correo para informar de nuevo artículo a los usuarios
    que así tengan configurado su perfil y a todos los miembros del staff"""
    for user in User.objects.all():
        if autor_id != user and user.perfil.mail_on_nuevo_articulo == True:
            subject = "ComunidadLSA, Se ha publicado un nuevo artículo."
            body = render_to_string(
                "mails/nuevo_articulo.html",
                {
                    "username": user.username,
                    "articulo_id": articulo_id,
                },
            )
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)


class TemaArticulo(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    descripcion_corta = models.CharField(
        max_length=300, verbose_name="Descripción corta"
    )
    descripcion = models.CharField(max_length=300, verbose_name="Descripción")

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Temas de artículos"


class ArticuloManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publico=True)


class Articulo(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Título")
    imagen = models.ImageField(upload_to="public/static/uploads/%Y/%m/%d/")
    entradilla = models.CharField(max_length=350, verbose_name="Entradilla")
    cuerpo = RichTextUploadingField(verbose_name="Cuerpo")
    publico = models.BooleanField(default=False, verbose_name="Publicar")
    autor = models.ForeignKey(
        User, verbose_name="Autor", on_delete=models.CASCADE)
    tema = models.ForeignKey(
        TemaArticulo, verbose_name="Tema", on_delete=models.CASCADE
    )
    fecha_creacion = models.DateTimeField(editable=False)
    fecha_modificacion = models.DateTimeField()
    # Utilizado para controlar si ya hemos notificado a los usuarios
    # de que se ha publicado este artículo.
    users_notified = models.BooleanField(
        default=False, editable=False, verbose_name="Han sido los usuarios notificados?"
    )

    objects = ArticuloManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name_plural = "Articulos"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return "{}".format(self.titulo)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.fecha_creacion = timezone.now()
        self.fecha_modificacion = timezone.now()
        super(Articulo, self).save(*args, **kwargs)
        if self.publico == True and self.users_notified == False:
            notify_new_article.delay(self.id, self.autor.id)
            self.users_notified = True
            self.save()
        return None


class ComentarioArticuloManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(censurado=False)


class ComentarioArticulo(models.Model):
    articulo = models.ForeignKey(
        Articulo,
        related_name="comentarios",
        verbose_name="Artículo",
        on_delete=models.CASCADE,
    )
    cuerpo = RichTextUploadingField(verbose_name="Cuerpo")
    autor = models.ForeignKey(
        User, verbose_name="Autor", on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(editable=False)
    fecha_modificacion = models.DateTimeField()
    censurado = models.BooleanField(default=False, verbose_name="Censurar")

    objects = ComentarioArticuloManager()
    all_objects = models.Manager()

    def __str__(self):
        return "{}...".format(self.cuerpo[0:50])

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.fecha_creacion = timezone.now()
        self.fecha_modificacion = timezone.now()
        return super(ComentarioArticulo, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Comentarios de artículos"
        ordering = ["fecha_creacion"]
