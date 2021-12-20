from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from blog.models import TemaArticulo, Articulo, ComentarioArticulo
from excel_response import ExcelResponse
from mailapp.utils import sendCustomMail
from mailapp.models import Plantilla


class UserAdmin(UserAdmin):
    actions = ["export_to_spreedsheet", "mail_seleccionados"]
    date_hierarchy = "date_joined"
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "mail_confirmado",
    )
    list_filter = (
        "perfil__mail_confirmado",
        "is_staff",
        "is_superuser",
        "groups__name",
    )

    def mail_confirmado(self, obj):
        return obj.perfil.mail_confirmado

    def export_to_spreedsheet(self, request, queryset):
        data = [
            [
                "id",
                "Nombre usuario",
                "Nombre",
                "Apellidos",
                "Email",
                "Staff?",
                "Cuenta activa?",
                "Super usuario?",
                "Último acceso",
                "Fecha de registro",
            ]
        ]
        for user in queryset:
            data.append(
                [
                    user.id,
                    user.username,
                    user.first_name,
                    user.last_name,
                    user.email,
                    user.is_staff,
                    user.is_active,
                    user.is_superuser,
                    user.last_login,
                    user.date_joined,
                ]
            )
        return ExcelResponse(data, "usuarios")

    export_to_spreedsheet.short_description = "Exportar a Hoja de cálculo"

    def mail_seleccionados(self, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect(
            "/sendmail/?ct=%s&ids=%s"
            % (
                ct.pk,
                ",".join(str(pk) for pk in selected),
            )
        )

    mail_seleccionados.short_description = "Enviar correo a selección"


class TemaArticuloAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion_corta")


class ComentarioInline(admin.TabularInline):
    model = ComentarioArticulo


class ArticuloAdmin(admin.ModelAdmin):
    date_hierarchy = "fecha_creacion"
    list_display = ("titulo", "autor", "tema", "fecha_creacion")
    search_fields = ["titulo", "autor__username"]
    list_filter = ("tema", "fecha_creacion", "publico")
    inlines = (ComentarioInline,)
    ordering = ("-fecha_creacion", "titulo")

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class ComentarioArticuloAdmin(admin.ModelAdmin):
    date_hierarchy = "fecha_creacion"
    list_display = ("autor", "comment_intro", "fecha_creacion", "censurado")
    search_fields = ("cuerpo", "autor__username")
    list_filter = ("articulo__tema",)
    ordering = ("-fecha_creacion", "autor__username")

    def comment_intro(self, obj):
        return "{}...".format(obj.cuerpo[0:20])

    comment_intro.short_description = "Comentario"

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(TemaArticulo, TemaArticuloAdmin)
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(ComentarioArticulo, ComentarioArticuloAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
