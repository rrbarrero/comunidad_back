from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from .models import Plantilla
from django.contrib.auth.models import User
from .utils import sendCustomMail


@login_required
def home(request):
    if request.POST:
        mailTemplate_id = request.POST.get("template_id", "")
        mailTemplate = get_object_or_404(Plantilla, pk=mailTemplate_id)
        users = [
            get_object_or_404(User, pk=x)
            for x in request.POST.get("ids", "").split(",")
        ]
        messages = 0
        for user in users:
            sendCustomMail(mailTemplate, user)
            messages += 1
        return render(
            request,
            "send_report.html",
            {
                "total_messages": messages,
            },
        )
    # modelName = request.GET.get('ct', '')
    usuarios = request.GET.get("ids")
    plantillas = Plantilla.objects.all()
    return render(
        request,
        "select_template.html",
        {
            "plantillas": plantillas,
            "usuarios_string": usuarios,
            "usuarios": usuarios.split(","),
        },
    )
