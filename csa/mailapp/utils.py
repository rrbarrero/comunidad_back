from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, Context


def sendCustomMail(mailTemplate, dstObject):
    t = Template(mailTemplate.body_content)
    c = Context({"usuario": dstObject})
    mailBody = t.render(c)
    send_mail(
        mailTemplate.asunto,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [dstObject.email],
        html_message=mailBody,
        fail_silently=False,
    )
