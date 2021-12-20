from django.urls import path, include
from django.conf.urls import include, url
from news import apiviews


urlpatterns = [
    path(
        "comentarios/<int:pk>",
        apiviews.ComentarioNoticiaDetailUpdate.as_view(),
        name="comentario_detail_update",
    ),
    path(
        "noticias/<int:pk>",
        apiviews.NoticiaDetail.as_view(),
        name="news_detail",
    ),
    path(
        "noticias/<int:pk>/comentarios",
        apiviews.ListCreateComentarioNoticia.as_view(),
        name="news_comments_list",
    ),
    path(
        "noticias/<str:posicion>/preview",
        apiviews.NoticiaPreview.as_view(),
        name="news_preview",
    ),
]
