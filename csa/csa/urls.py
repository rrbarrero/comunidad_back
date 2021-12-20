"""csa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls import include, url
from django.conf.urls.static import static
from userprofile import views as userProfileViews


urlpatterns = [
    path("admin/", admin.site.urls),
    #    path("tinymce/", include("tinymce.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    url("avatar/", include("avatar.urls")),
    path("v1/news/", include("news.urls")),
    path("v1/blog/", include("blog.urls")),
    path("v1/usuarios/", include("userprofile.urls")),
    path("v1/foro/", include("foro.urls")),
    path("confirmar/<uuid:accountUuid>/", userProfileViews.mail_confirmation),
    path("sendmail/", include("mailapp.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if os.uname()[1] in ("pc01", "pc02", "mjrltp", "PC10348", "rz01"):
    import debug_toolbar

    urlpatterns = [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
