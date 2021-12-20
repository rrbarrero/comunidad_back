from datetime import datetime
import bleach

from django.contrib.auth.models import User
from rest_framework import serializers

from news.models import Noticia, ComentarioNoticia


class NoticiaSerializer(serializers.HyperlinkedModelSerializer):

    autor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Noticia
        fields = [
            "id",
            "titulo",
            "posicion",
            "imagen",
            "entradilla",
            "cuerpo",
            "autor",
            "fecha_creacion",
            "fecha_modificacion",
        ]
        extra_kwargs = {
            "fecha_creacion": {"read_only": True},
            "fecha_modificacion": {"read_only": True},
        }


class ComentarioNoticiaSerializer(serializers.HyperlinkedModelSerializer):

    noticia = serializers.PrimaryKeyRelatedField(queryset=Noticia.objects.all())
    autor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate_cuerpo(self, value):
        return bleach.clean(value)

    class Meta:
        model = ComentarioNoticia
        fields = [
            "id",
            "noticia",
            "cuerpo",
            "autor",
            "fecha_creacion",
            "fecha_modificacion",
        ]
        extra_kwargs = {
            "autor": {"read_only": True},
            "noticia": {"read_only": True},
            "fecha_creacion": {"read_only": True},
            "fecha_modificacion": {"read_only": True},
        }