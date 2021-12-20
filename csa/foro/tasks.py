from django.core.mail import send_mail
from csa.celery import app as celery_app
from django.contrib.auth.models import User
from foro.models import ComentarioPublicacion, Publicacion
from django.conf import settings
from django.template.loader import render_to_string
from csa.pub import publish_event


@celery_app.task
def send_async_mail(subject, body, dst):
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [dst], fail_silently=False)


@celery_app.task
def notify_new_comment(comment_id):
    """Envía notificación de nuevo comentario sí:
    1.- Está en el hilo y tiene activado notificar.
    2.- Es miembro del staff
    3.- Al dueño del hilo.
    """
    try:
        comment = ComentarioPublicacion.objects.get(pk=comment_id)
    except ComentarioPublicacion.DoesNotExist:
        return
    publish_event("FORO.TASKS.notify_new_comment", {"id": comment_id})
    recipients = []
    recipients.append(comment.publicacion.autor)
    for cmnt in comment.publicacion.comentarios.all():
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
            "mails/nuevo_comentario_foro.html",
            {
                "username": user.username,
                "post_id": comment.publicacion.id,
            },
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


@celery_app.task
def notify_new_hilo(hilo_id):
    """ Notifica a todos los miembros del staff """
    try:
        publicacion = Publicacion.objects.get(pk=hilo_id)
    except Publicacion.DoesNotExist:
        return
    for user in User.objects.filter(is_staff=True):
        if user != publicacion.autor:
            subject = "ComunidadLSA, se ha publicado un nuevo hilo."
            body = render_to_string(
                "mails/nuevo_hilo.html",
                {
                    "username": user.username,
                    "post_id": publicacion.id,
                },
            )
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
