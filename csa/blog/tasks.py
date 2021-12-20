from django.core.mail import send_mail
from csa.celery import app as celery_app
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from blog.models import ComentarioArticulo


@celery_app.task
def send_async_mail(subject, body, dst):
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [dst], fail_silently=False)


@celery_app.task
def notify_new_comment(comment_id):
    """Notifica cuando se publica un nuevo comentario en un artículo:
    1.- Al autor del artículo.
    2.- A todos los intervinientes si tienen activada la opción de notificación
    de nuevos comentarios.
    3.- A todos los miembros del staff"""
    try:
        comment = ComentarioArticulo.objects.get(pk=comment_id)
    except ComentarioArticulo.DoesNotExist:
        return
    recipients = []
    recipients.append(comment.articulo.autor)
    for cmnt in comment.articulo.comentarios.all():
        if cmnt.autor != comment.autor:
            if cmnt.autor.perfil.mail_on_nuevo_comentario == True:
                recipients.append(cmnt.autor)
    for user in User.objects.filter(is_staff=True):
        if user != comment.autor:
            if user.perfil.mail_on_nuevo_comentario == True:
                recipients.append(user)
    for user in list(set(recipients)):
        subject = "ComunidadLSA, tienes un nuevo comentario"
        body = render_to_string(
            "mails/nuevo_comentario_articulo.html",
            {
                "username": user.username,
                "articulo_id": comment.articulo.id,
            },
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
