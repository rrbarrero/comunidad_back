from django.core.mail import send_mail
from csa.celery import app as celery_app
from django.conf import settings

@celery_app.task
def send_async_mail(subject, body, dst):
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [dst], fail_silently=False)


def mail_to_admin(subject, body):
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, ["admin@comunidadlsa.es"], fail_silently=False)


@celery_app.task
def confirmation_mail_notification(username, email, profileHash):
    subject = "Bienvenido a la Comunidad de la Sociedad del Aprendizaje"
    body = "Solo falta un último paso para comenzar el cambio, confirma tu "
    body += (
        "dirección de correo haciendo click en el siguiente enlace https://comunidadlsa.es/confirmar/{}/".format(
            profileHash
        )
    )
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    mail_to_admin(
            "Se ha registrado un nuevo usuario",
            "Se ha registro un nuevo usuario: {}, correo: {}.".format(
                username, email
            ))