from django.urls import path, include
from django.conf.urls import include, url
from blog import apiviews


urlpatterns = [
    path(
        "comentarios/<int:pk>",
        apiviews.ComentarioArticuloDetailUpdate.as_view(),
        name="comentario_detail_update",
    ),
    path(
        "articulos/<int:pk>/comentarios",
        apiviews.ListCreateComentarioArticulo.as_view(),
        name="articles_comments_list",
    ),
    path(
        "articulos/<int:pk>",
        apiviews.ArticuloDetail.as_view(),
        name="articles_detail",
    ),
    path(
        "articulos",
        apiviews.ArticuloList.as_view(),
        name="articles_list",
    ),
]
