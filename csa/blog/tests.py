from datetime import datetime
from django.urls import reverse
from django.core import mail
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.models import TemaArticulo, Articulo, ComentarioArticulo


class ComentarioArticuloTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            "admin",
            "testing@admin.com",
            make_password("olakdise_"),
        )
        self.assertIn("testing@admin.com", mail.outbox[0].to)
        self.user = User.objects.create_user(
            username="julio",
            email="testing@user.com",
            password=make_password("iglesias"),
        )
        self.assertIn("testing@user.com", mail.outbox[1].to)
        self.assertEqual(2, User.objects.all().count())
        tema = TemaArticulo.objects.create(
            nombre="Tema 1",
            descripcion_corta="Descripción corta del tema 1",
            descripcion="Descripción larga del tema 1",
        )
        image_path = "{}/1.png".format(settings.DEFAULT_AVATARS_PATH)
        self.articulo = Articulo.objects.create(
            titulo="Articulo 1 title",
            imagen=SimpleUploadedFile(
                name="1.png",
                content=open(image_path, "rb").read(),
                content_type="image/jpeg",
            ),
            entradilla="Entradilla",
            cuerpo="Cuerpo",
            publico=True,
            autor=self.user,
            tema=tema,
            fecha_modificacion=datetime.now(),
        )
        self.comentario = ComentarioArticulo.objects.create(
            articulo=self.articulo,
            cuerpo="comentario 1",
            autor=self.user,
        )
        self.assertEqual(1, Articulo.objects.all().count())
        self.assertEqual(1, ComentarioArticulo.objects.all().count())

    def test_any_user_can_view_a_comment(self):
        url = reverse("comentario_detail", args=[self.comentario.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("comentario 1", response.data["cuerpo"])

    def test_logged_user_cannot_update_not_own_comment(self):
        """
        Ensure logged user cannot update another user comment
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " +
                           self.admin.auth_token.key)
        url = reverse("comentario_detail", args=[self.comentario.id])
        data = {
            "cuerpo": "comentario 2",
            "articulo": self.articulo.id,
            "autor": self.admin.id,
        }
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(url, format="json")
        self.assertEqual("comentario 1", response.data["cuerpo"])

    def test_logged_user_can_update_him_own_comment(self):
        """
        Ensure logged user can update own comments
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " +
                           self.user.auth_token.key)
        url = reverse("comentario_detail", args=[self.comentario.id])
        data = {
            "cuerpo": "comentario 2",
            "articulo": self.articulo.id,
            "autor": self.user.id,
        }
        response = client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, format="json")
        self.assertEqual("comentario 2", response.data["cuerpo"])
