import uuid
import logging
from random import randrange
from django.db import models

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# from django.core.mail import send_mail
from userprofile.tasks import confirmation_mail_notification
from django.utils.html import strip_tags
from django.conf import settings
from avatar.models import Avatar

# from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class Perfil(models.Model):
    user = models.OneToOneField(
        User,
        related_name="perfil",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    ocupacion = models.CharField(max_length=300, verbose_name="Ocupación", blank=True)
    frase_inspiradora = models.CharField(
        max_length=200, verbose_name="Frase inspiradora", blank=True
    )
    mail_confirmado = models.BooleanField(default=False, verbose_name="Mail confirmado")
    cuenta_desactivada = models.BooleanField(
        default=False, verbose_name="Cuenta desactivada"
    )
    confirmation_hash = models.UUIDField(default=uuid.uuid4, unique=True)
    mail_on_nuevo_articulo = models.BooleanField(
        default=True, verbose_name="Notificar con nuevo artículo"
    )
    mail_on_nuevo_comentario = models.BooleanField(
        default=True, verbose_name="Notificar con nuevo comentario"
    )
    mail_on_nuevo_evento = models.BooleanField(
        default=True, verbose_name="Notificar con nuevo evento"
    )

    def __str__(self):
        return "{}, {}".format(self.user.username, self.mail_confirmado)

    class Meta:
        verbose_name_plural = "Perfiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        perfil = Perfil.objects.create(user=instance)
        confirmation_mail_notification.delay(instance.username, instance.email, instance.perfil.confirmation_hash)
    instance.perfil.save()


@receiver(post_save, sender=User)
def create_user_avatar(sender, instance, created, **kwargs):
    if created:
        avatar = Avatar.objects.create(
            user=instance,
            primary=True,
            avatar="avatars/defaults/{}.svg".format(randrange(1, 26)),
        )
    instance.avatar_set.first().save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
