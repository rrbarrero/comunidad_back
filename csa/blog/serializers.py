from datetime import datetime
import bleach

from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import TemaArticulo, Articulo, ComentarioArticulo


class TemaArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemaArticulo
        fields = ["nombre", "descripcion_corta", "descripcion"]


class ArticuloSerializer(serializers.HyperlinkedModelSerializer):

    autor = serializers.PrimaryKeyRelatedField(read_only=True)
    tema = TemaArticuloSerializer()

    class Meta:
        model = Articulo
        fields = [
            "id",
            "titulo",
            "imagen",
            "entradilla",
            "cuerpo",
            "autor",
            "tema",
            "fecha_creacion",
            "fecha_modificacion",
        ]
        extra_kwargs = {
            "fecha_creacion": {"read_only": True},
            "fecha_modificacion": {"read_only": True},
        }


class ComentarioArticuloSerializer(serializers.HyperlinkedModelSerializer):

    articulo = serializers.PrimaryKeyRelatedField(queryset=Articulo.objects.all())
    autor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate_cuerpo(self, value):
        return bleach.clean(value)

    class Meta:
        model = ComentarioArticulo
        fields = [
            "id",
            "articulo",
            "cuerpo",
            "autor",
            "fecha_creacion",
            "fecha_modificacion",
        ]
        extra_kwargs = {
            "autor": {"read_only": True},
            "articulo": {"read_only": True},
            "fecha_creacion": {"read_only": True},
            "fecha_modificacion": {"read_only": True},
        }