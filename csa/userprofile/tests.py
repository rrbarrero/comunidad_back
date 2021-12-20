import json
from collections import OrderedDict
from django.core import mail
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from avatar.models import Avatar
from rest_framework.authtoken.models import Token
from django.conf import settings


class UserTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            "admin",
            "testing@admin.com",
            make_password("olakdise_"),
        )
        self.assertIn("testing@admin.com", mail.outbox[0].to)

    def test_create_user(self):
        """
        Ensure we can create a new user account.
        """
        url = reverse("user_register")
        data = {
            "username": "hola",
            "first_name": "hola",
            "last_name": "adios",
            "email": "micorreo@gmail.com",
            "password": make_password("olakdise_"),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, User.objects.all().count())
        self.assertEqual(
            response.data,
            {
                "id": response.data["id"],
                "username": "hola",
                "first_name": "hola",
                "last_name": "adios",
                "perfil": OrderedDict([("frase_inspiradora", "")]),
            },
        )
        self.assertIn("micorreo@gmail.com", mail.outbox[1].to)
        self.assertEqual(len(mail.outbox), 2)

    def test_unathorized_cant_update_user(self):
        """
        Ensure we cant update a user account when not auth.
        """
        user = User.objects.create(
            username="hola", password=make_password("olakdise_"))
        url = reverse("user_detail", args=[user.id])
        data = {
            "username": "adios",
            "first_name": "adios",
            "last_name": "hola",
            "email": "micorreo@gmail.com",
            "password": make_password("olakdise_"),
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(mail.outbox), 1)

    def test_authenticated_user_cant_update_another(self):
        """
        Ensure we cant update another user account even auth.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " +
                           self.admin.auth_token.key)
        user = User.objects.create(
            username="hola", password=make_password("olakdise_"))
        url = reverse("user_detail", args=[user.id])
        data = {
            "username": "adios",
            "first_name": "adios",
            "last_name": "hola",
            "email": "micorreo@gmail.com",
            "password": make_password("olakdise_"),
        }
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(mail.outbox), 1)

    def test_authenticated_user_can_update_himself(self):
        """
        Ensure we can update our profile when auth.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " +
                           self.admin.auth_token.key)
        url = reverse("user_detail", args=[self.admin.id])
        data = {
            "username": "admin",
            "first_name": "adios",
            "last_name": "hola",
            "email": "admin@gmail.com",
            "password": make_password("olakdise_"),
        }
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get(url, format="json")
        self.assertEqual(
            response.data,
            {
                "id": self.admin.id,
                "username": "admin",
                "first_name": "adios",
                "last_name": "hola",
                "perfil": OrderedDict([("frase_inspiradora", "")]),
            },
        )
        self.assertEqual(len(mail.outbox), 1)

    def test_anonym_can_view_user_avatar(self):
        """
        Ensure anonymous users can view avatars
        """
        user = User.objects.create_user(
            username="julio",
            email="testing@admin.com",
            password=make_password("iglesias"),
        )
        self.assertIn("testing@admin.com", mail.outbox[0].to)
        avatar = Avatar.objects.filter(user=user).first()
        url = reverse("avatar_detail", args=[user.id])
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.data,
            {"avatar": "/" + str(avatar.avatar), "user": user.id},
        )

    def test_logged_user_can_update_him_avatar(self):
        """
        Ensure logged user can update him avatar
        """
        user = User.objects.create_user(
            username="julio",
            email="testing@admin.com",
            password=make_password("iglesias"),
        )
        image_path = "{}/1.png".format(settings.DEFAULT_AVATARS_PATH)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + user.auth_token.key)
        url = reverse("avatar_detail", args=[user.id])
        with open(image_path, "rb") as image_file:
            data = {"avatar": image_file, "user": user.id}
            response = client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, format="json")
        avatar = Avatar.objects.filter(user=user).first()
        self.assertEqual(
            response.data,
            {"avatar": "/" + str(avatar.avatar), "user": user.id},
        )

    def test_logged_user_cannot_update_another_user_avatar(self):
        """
        Ensure logged user cannot update another user avatar's
        """
        user = User.objects.create_user(
            username="julio",
            email="testing@admin.com",
            password=make_password("iglesias"),
        )
        image_path = "{}/1.png".format(settings.DEFAULT_AVATARS_PATH)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + user.auth_token.key)
        url = reverse("avatar_detail", args=[self.admin.id])
        with open(image_path, "rb") as image_file:
            data = {"avatar": image_file, "user": user.id}
            response = client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(url, format="json")
        avatar = Avatar.objects.filter(user=self.admin).first()
        self.assertEqual(
            response.data,
            {"avatar": "/" + str(avatar.avatar), "user": self.admin.id},
        )
