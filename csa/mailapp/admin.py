from django.contrib import admin
from .models import *


class PlantillaAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "identificador": ("nombre",),
    }
    list_display = ("nombre", "asunto")


admin.site.register(Plantilla, PlantillaAdmin)
