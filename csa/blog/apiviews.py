from datetime import datetime, timedelta
from django.http import Http404
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import permissions
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

from blog.models import Articulo, ComentarioArticulo
from blog.serializers import (
    ArticuloSerializer,
    ComentarioArticuloSerializer,
)
from blog.tasks import notify_new_comment


class ArticuloList(generics.ListAPIView):
    """
    Returns a list of all **published** articles.

    """

    queryset = Articulo.objects.filter(publico=True).all()
    serializer_class = ArticuloSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArticuloDetail(generics.RetrieveAPIView):
    """
    Returns a single **published** articles.

    """

    queryset = Articulo.objects.filter(publico=True).all()
    serializer_class = ArticuloSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListCreateComentarioArticulo(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    Returns a list of non censured comments of an article.

    """

    serializer_class = ComentarioArticuloSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Articulo.objects.get(pk=self.articulo_id).comentarios.all()

    def get(self, request, pk):
        self.articulo_id = pk
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
            ComentarioArticulo.objects.filter(autor=request.user)
            .filter(fecha_creacion__gt=time_threshold)
            .count()
        )
        if last_comments >= rate_limit_comments:
            content = {
                "No permitido": "Tranquilo vaquero. Deja enfríar un poco las pistolas."
            }
            return Response(content, status.HTTP_403_FORBIDDEN)
        response = self.create(request, *args, **kwargs)
        comentario_id = ComentarioArticulo.objects.all().last().id
        notify_new_comment.delay(comentario_id)
        return response
        


class ComentarioArticuloDetailUpdate(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    queryset = ComentarioArticulo.objects.all()
    serializer_class = ComentarioArticuloSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, pk=None):
        instance = None
        try:
            instance = ComentarioArticulo.objects.get(pk=pk)
        except ComentarioArticulo.DoesNotExist:
            raise Http404
        if instance.autor.id != request.user.id:
            content = {"No permitido": "Sin permiso para la operación"}
            return Response(content, status.HTTP_403_FORBIDDEN)
        serializer = ComentarioArticuloSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
