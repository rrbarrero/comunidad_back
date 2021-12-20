import uuid
import logging
from django.http import Http404
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from avatar.models import Avatar
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import permissions
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# from django.core.mail import send_mail
from userprofile.tasks import send_async_mail
from csa.pub import publish_event
from userprofile.models import Perfil
from userprofile.serializers import (
    UserSerializer,
    AvatarSerializer,
    UserNonDiscreteSerializer,
)

logger = logging.getLogger(__name__)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.perfil.mail_confirmado == False:
            content = {"No permitido": "El correo no ha sido confirmado."}
            return Response(content, status.HTTP_403_FORBIDDEN)
        if user.perfil.cuenta_desactivada == True:
            content = {"No permitido": "La cuenta ha sido deshabilitada."}
            return Response(content, status.HTTP_403_FORBIDDEN)
        token, created = Token.objects.get_or_create(user=user)
        publish_event("USERPROFILE.APIVIEWS.CustomAuthToken", {"id": user.id})
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class UserDetail(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    Request user info.

    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserNonDiscriteDetailUpdate(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):

    """Utilizada para llamadas no discreta. Devuelve datos
    sensibles"""

    queryset = User.objects.all()
    serializer_class = UserNonDiscreteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        instance = None
        if request.user.id != pk:
            content = {"No permitido": "Sin permiso para la operación"}
            return Response(content, status.HTTP_403_FORBIDDEN)
        try:
            instance = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        serializer = UserNonDiscreteSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk=None):
        instance = None
        if request.user.id != pk:
            content = {"No permitido": "Sin permiso para la operación"}
            return Response(content, status.HTTP_403_FORBIDDEN)
        try:
            instance = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        if "password" in request.data:
            serializer = UserNonDiscreteSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            instance.set_password(request.data["password"])
            instance.save()
        else:
            serializer = UserSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
        profile = request.data["perfil"]
        instance.perfil.frase_inspiradora = profile["frase_inspiradora"]
        instance.perfil.mail_on_nuevo_articulo = profile["mail_on_nuevo_articulo"]
        instance.perfil.mail_on_nuevo_comentario = profile["mail_on_nuevo_comentario"]
        instance.perfil.save()
        publish_event(
            "USERPROFILE.APIVIEWS.UserNonDiscriteDetailUpdate", {"id": instance.id}
        )
        return Response(serializer.data)


class UserSearch(generics.ListAPIView):
    """Para buscar usuario por email. Utilizado para
    la plataforma de inscripción al 4º Congreso"""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()

    def get_queryset(self):
        query = self.request.query_params.get("email", None)
        if query is None:
            return User.objects.none()
        return User.objects.filter(email__icontains=query)


class UserCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    """
    Register a new user
    """

    # TODO: SI UN USUARIO ESTA LOGADO NO DEBERÍA PODER REGISTRARSE
    queryset = User.objects.all()
    serializer_class = UserNonDiscreteSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        if User.objects.filter(email=email).count() > 0:
            content = {
                "No permitido": "Ya existe una cuenta con esa dirección de correo."
            }
            return Response(content, status.HTTP_403_FORBIDDEN)
        instance = serializer.save()
        instance.set_password(password)
        instance.save()
        # TODO: ESTO TIENE QUE DEVOLVER 201, COMPROBAR EL RESTO
        publish_event("USERPROFILE.APIVIEWS.UserCreate", {"id": instance.id})
        return Response(serializer.data)


class AvatarDetail(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    """
    Avatar detail and update
    """

    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        user = None
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        instance = Avatar.objects.filter(user=user).first()
        serializer = AvatarSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if request.user.id != pk:
            content = {"No permitido": "Sin permiso para la operación"}
            return Response(content, status.HTTP_403_FORBIDDEN)
        instance = Avatar.objects.filter(user=request.user).first()
        serializer = AvatarSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PaswordRecover(mixins.UpdateModelMixin, generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]

    def put(self, request):
        email = request.data["email"]
        try:
            validate_email(email)
        except ValidationError as e:
            content = {"No permitido": e}
            return Response(content, status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            content = {
                "No permitido": "No existe ninguna cuenta asociada a ese correo."
            }
            return Response(content, status.HTTP_404_NOT_FOUND)
        logger.warning(
            "Solicitada restauración de contraseña para el usuario {}".format(
                user.username
            )
        )
        user.perfil.confirmation_hash = uuid.uuid4()
        user.perfil.save()
        body = "Hola has solicitado restear tu contraseña, si es así pincha "
        body += "en el siguiente enlace: https://comunidadlsa.es/pass_recover/{} Si no has sido tu, simplemente borra ".format(
            user.perfil.confirmation_hash
        )
        body += "este correo.\n\nRecuerda que tu nombre de usuario es: {}".format(
            user.username
        )
        send_async_mail.delay(
            "Comunidad Sociedad del Aprendizaje. Recupera tu contraseña.",
            body,
            user.email,
        )
        send_async_mail.delay(
            "Solicitud de recuperación de contraseña.",
            (
                "Se ha solicitado un envío de recuperación de contraseña para el correo: "
                "{}".format(user.email)
            ),
            "admin@comunidadlsa.es",
        )
        return Response("success", status.HTTP_200_OK)


class PaswordChange(mixins.UpdateModelMixin, generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]

    def validate_password(self, value):
        if value.isalnum():
            return False
        if 8 > len(value) or len(value) > 16:
            return False
        return True

    def put(self, request):
        profileUuid = request.data["uuid"]
        password = request.data["password"]
        if not self.validate_password(password):
            content = {
                "Error": "La contraseña tiene que tener entre 9 y 15 carácteres y alguno especial como +-.="
            }
            return Response(content, status.HTTP_403_FORBIDDEN)
        try:
            perfil = Perfil.objects.get(confirmation_hash=profileUuid)
        except Perfil.DoesNotExist:
            content = {
                "Error": "Se ha producido un error al restaurar la contraseña. Este código ya no es válido. Vuelva a solicitar la recuperación."
            }
            return Response(content, status.HTTP_404_NOT_FOUND)
        newUuid = uuid.uuid4()
        perfil.confirmation_hash = str(newUuid)
        perfil.user.set_password(password)
        perfil.save()
        perfil.user.save()
        return Response("Success", status.HTTP_200_OK)
