from django.contrib import admin
from django.urls import reverse
from foro.models import TemaForo, Publicacion, ComentarioPublicacion


class TemaForoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion_corta")


class ComentarioInline(admin.TabularInline):
    model = ComentarioPublicacion


class PublicacionAdmin(admin.ModelAdmin):
    date_hierarchy = "fecha_creacion"
    list_display = ("titulo", "autor", "censurado", "fecha_creacion")
    search_fields = ("titulo", "autor__username")
    list_filter = ("tema", "fecha_creacion")
    inlines = [ComentarioInline]
    ordering = ("-fecha_creacion", "titulo")

    def view_on_site(self, obj):
        return "/hilos/{}".format(obj.id)

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class ComentarioPublicacionAdmin(admin.ModelAdmin):
    date_hierarchy = "fecha_creacion"
    list_display = ("autor", "comment_intro", "fecha_creacion", "censurado")
    search_fields = ("cuerpo", "autor__username")
    list_filter = ("publicacion__tema",)
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


admin.site.register(TemaForo, TemaForoAdmin)
admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(ComentarioPublicacion, ComentarioPublicacionAdmin)