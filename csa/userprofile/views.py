from django.shortcuts import redirect, render
from userprofile.models import Perfil
from django.shortcuts import get_object_or_404
from django.conf import settings
from userprofile.tasks import send_async_mail



def mail_confirmation(request, accountUuid):
    perfil = get_object_or_404(Perfil, confirmation_hash=accountUuid)
    perfil.mail_confirmado = True
    perfil.save()
    # return redirect(settings.SITE_PUBLIC_LOGIN)
    return render(request, "confirmation_success.html")
