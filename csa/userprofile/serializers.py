from django.contrib.auth.models import User

from userprofile.models import Perfil
from rest_framework import serializers
from avatar.models import Avatar


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = [
            "frase_inspiradora",
            "mail_on_nuevo_articulo",
            "mail_on_nuevo_comentario",
            "mail_on_nuevo_evento",
        ]


class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)

    def validate_password(self, value):
        if value.isalnum():
            raise serializers.ValidationError(
                "La contraseña debe tener, al menos, un carácter especial."
            )
        return value

    class Meta:
        model = User
        fields = [
            "id",
            "perfil",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            # "password",
            # "email",
        ]

        # extra_kwargs = {"password": {"write_only": True}, "email": {"write_only": True}}


class UserNonDiscreteSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)

    def validate_password(self, value):
        if value.isalnum():
            raise serializers.ValidationError(
                "La contraseña debe tener, al menos, un carácter especial como: +-."
            )
        return value

    class Meta:
        model = User
        fields = [
            "id",
            "perfil",
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
        ]


class AvatarSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Avatar
        fields = ["avatar", "user", "primary"]
        extra_kwargs = {"primary": {"write_only": True}}
