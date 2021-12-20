from datetime import datetime, timedelta
from django.conf import settings
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions, mixins, generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from news.models import Noticia, ComentarioNoticia
from news.serializers import (
    NoticiaSerializer,
    ComentarioNoticiaSerializer,
)
from news.tasks import notify_new_comment


class LargeResultsSetPagination(PageNumberPagination):
    max_page_size = 100
    page_size_query_param = "page_size"


class NoticiaPreview(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Returns a single **published** new.

    """

    queryset = Noticia.objects.filter(publico=True).all()
    serializer_class = NoticiaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, posicion):
        queryset = self.get_queryset().filter(posicion=posicion).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class NoticiaDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Returns a single **published** new.

    """

    queryset = Noticia.objects.filter(publico=True).all()
    serializer_class = NoticiaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ListCreateComentarioNoticia(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    Returns a list of non censured comments of an article.

    """

    serializer_class = ComentarioNoticiaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Noticia.objects.get(pk=self.noticia_id).comentarios.all()

    def get(self, request, pk):
        self.noticia_id = pk
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
            ComentarioNoticia.objects.filter(autor=request.user)
            .filter(fecha_creacion__gt=time_threshold)
            .count()
        )
        if last_comments >= rate_limit_comments:
            content = {
                "No permitido": "Tranquilo vaquero. Deja enfríar un poco las pistolas."
            }
            return Response(content, status.HTTP_403_FORBIDDEN)
        response = self.create(request, *args, **kwargs)
        comentario_id = ComentarioNoticia.objects.all().last().id
        notify_new_comment.delay(comentario_id)
        return response


class ComentarioNoticiaDetailUpdate(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    queryset = ComentarioNoticia.objects.all()
    serializer_class = ComentarioNoticiaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, pk=None):
        instance = None
        try:
            instance = ComentarioNoticia.objects.get(pk=pk)
        except ComentarioNoticia.DoesNotExist:
            raise Http404
        if instance.autor.id != request.user.id:
            content = {"No permitido": "Sin permiso para la operación"}
            return Response(content, status.HTTP_403_FORBIDDEN)
        serializer = ComentarioNoticiaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)