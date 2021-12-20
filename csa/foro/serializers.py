from datetime import datetime
import bleach
from django.contrib.auth.models import User
from rest_framework import serializers
from foro.models import TemaForo, Publicacion, ComentarioPublicacion


class TemaForoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemaForo
        fields = [
            "id",
            "nombre",
            "imagen",
            "descripcion_corta",
            "descripcion",
        ]


class PublicacionSerializer(serializers.HyperlinkedModelSerializer):

    autor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tema = serializers.PrimaryKeyRelatedField(queryset=TemaForo.objects.all())

    def validate_cuerpo(self, value):
        return bleach.clean(value)

    class Meta:
        model = Publicacion
        fields = [
            "id",
            "titulo",
            "cuerpo",
            "autor",
            "tema",
            "lecturas",
            "fecha_creacion",
            "fecha_modificacion",
        ]
        extra_kwargs = {
            "fecha_creacion": {"read_only": True},
            "fecha_modificacion": {"read_only": True},
            "lecturas": {"read_only": True},
        }


class ComentarioPublicacionSerializer(serializers.HyperlinkedModelSerializer):

    publicacion = serializers.PrimaryKeyRelatedField(queryset=Publicacion.objects.all())
    autor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate_cuerpo(self, value):
        return bleach.clean(value)

    class Meta:
        model = ComentarioPublicacion
        fields = [
            "id",
            "publicacion",
            "cuerpo",
            "autor",
            "fecha_creacion",
            "fecha_modificacion",
        ]
        extra_kwargs = {
            "autor": {"read_only": True},
            "publicacion": {"read_only": True},
            "fecha_creacion": {"read_only": True},
            "fecha_modificacion": {"read_only": True},
        }
