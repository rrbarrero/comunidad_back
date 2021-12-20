from datetime import datetime, timedelta
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import Count
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from csa.pub import publish_event
from foro.tasks import notify_new_comment, notify_new_hilo

# from foro.permissions import PublicacionPermission

from foro.models import TemaForo, Publicacion, ComentarioPublicacion
from foro.serializers import (
    TemaForoSerializer,
    PublicacionSerializer,
    ComentarioPublicacionSerializer,
)


class TemaForoList(generics.ListAPIView):
    """
    Return a list of all temas
    """

    queryset = TemaForo.objects.all()
    serializer_class = TemaForoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TemaForoDetail(generics.RetrieveAPIView):
    """
    Returns a single **published** articles.

    """

    queryset = TemaForo.objects.all()
    serializer_class = TemaForoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListCreatePublicaciones(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):

    """
    List publicaciones
    """

    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return TemaForo.objects.get(pk=self.temaForo_id).publicaciones.all()

    def get(self, request, pk):
        self.temaForo_id = pk
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        notify_new_hilo.delay(Publicacion.objects.first().id) # first por el order por defecto
        return response


class DetailUpdatePublicaciones(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):

    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Publicacion.objects.all()

    def get(self, request, pk=None):
        instance = None
        try:
            instance = Publicacion.objects.get(pk=pk)
        except Publicacion.DoesNotExist:
            raise Http404
        instance.lecturas += 1
        instance.save()
        serializer = PublicacionSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk=None):
        instance = None
        try:
            instance = Publicacion.objects.get(pk=pk)
        except Publicacion.DoesnotExist:
            raise Http404
        # TODO Devolver 403 antes de la consulta, no es necesario
        # ver userprofile.apiviews.UserNonDiscreteDetail.get
        if instance.autor.id != request.user.id:
            content = {"No permitido": "Sin permiso para la operación"}
            return Response(content, status.HTTP_403_FORBIDDEN)
        serializer = PublicacionSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ListCreateComentarioPublicacion(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):

    """
    List comments of publication
    """

    serializer_class = ComentarioPublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Publicacion.objects.get(pk=self.publicacion_id).comentarios.all()

    def get(self, request, pk):
        self.publicacion_id = pk
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        rate_limit_comments, rate_limit_time = settings.MAX_COMMENTS_PER_TIME
        time_threshold = datetime.now() - timedelta(minutes=rate_limit_time)
        last_comments = (
            ComentarioPublicacion.objects.filter(autor=request.user)
            .filter(fecha_creacion__gt=time_threshold)
            .count()
        )
        if last_comments >= rate_limit_comments:
            content = {
                "No permitido": "Tranquilo vaquero. Deja enfríar un poco las pistolas."
            }
            return Response(content, status.HTTP_403_FORBIDDEN)
        response = self.create(request, *args, **kwargs)
        # TODO CONSEGUIR EL COMENTARIO DE MANERA MÁS SEGURA AL CREARLO
        notify_new_comment.delay(request.user.comentariopublicacion_set.last().id)
        publish_event(
            "FORO.APIVIEWS.ListCreateComentarioPublicacion",
            {"id": request.user.comentariopublicacion_set.last().id},
        )
        return response


class DetailUpdateComentariosPublicaciones(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):

    serializer_class = ComentarioPublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ComentarioPublicacion.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, pk=None):
        instance = None
        try:
            instance = ComentarioPublicacion.objects.get(pk=pk)
        except ComentarioPublicacion.DoesnotExist:
            raise Http404
        if instance.autor.id != request.user.id:
            content = {"No permitido": "Sin permiso para la operación"}
            return Response(content, status.HTTP_403_FORBIDDEN)
        serializer = ComentarioPublicacionSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ListTopCommentsInPublicacion(generics.ListAPIView):

    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Publicacion.objects.annotate(count=Count("comentarios")).order_by(
        "-count"
    )[0:5]


class ListPublicationsWithLastComments(generics.ListAPIView):
    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = list(
        set(
            [
                x.publicacion
                for x in ComentarioPublicacion.objects.all().order_by(
                    "-fecha_creacion"
                )[0:5]
            ]
        )
    )
    queryset.reverse()


class ListPublicationsRecents(generics.ListAPIView):
    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Publicacion.objects.all()[0:5]