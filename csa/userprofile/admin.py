from django.contrib import admin
from userprofile.models import Perfil


class PerfilAdmin(admin.ModelAdmin):
    list_display = ("get_username", "get_email", "mail_confirmado", "get_date_joined")
    search_fields = ("user__username", "confirmation_hash")

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "username"
    get_username.admin_order_field = "user__username"

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "email"
    get_email.admin_order_field = "user__email"

    def get_date_joined(self, obj):
        return obj.user.date_joined

    get_date_joined.short_description = "Fecha_inscripcion"
    get_date_joined.admin_order_field = "user__date_joined"


admin.site.register(Perfil, PerfilAdmin)