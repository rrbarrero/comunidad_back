from django.contrib import admin
from news.models import Noticia, ComentarioNoticia


class ComentarioInline(admin.TabularInline):
    model = ComentarioNoticia


class NoticiaAdmin(admin.ModelAdmin):
    date_hierarchy = "fecha_creacion"
    list_display = ("titulo", "posicion", "autor", "fecha_creacion")
    search_fields = ("titulo", "autor__username")
    list_filter = ("posicion", "fecha_creacion", "publico")
    inlines = (ComentarioInline,)
    ordering = ("-fecha_creacion", "titulo")

    def view_on_site(self, obj):
        return "/portadas/{}".format(obj.id)

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class ComentarioNoticiaAdmin(admin.ModelAdmin):
    date_hierarchy = "fecha_creacion"
    list_display = ("autor", "comment_intro", "fecha_creacion", "censurado")
    search_fields = ("cuerpo", "autor__username")
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


admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(ComentarioNoticia, ComentarioNoticiaAdmin)
