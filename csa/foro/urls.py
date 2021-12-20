from django.urls import path, include
from foro import apiviews

urlpatterns = [
    path(
        "temas/<int:pk>/publicaciones",
        apiviews.ListCreatePublicaciones.as_view(),
        name="publicacion_list_create",
    ),
    path(
        "publicaciones/<int:pk>/comentarios",
        apiviews.ListCreateComentarioPublicacion.as_view(),
        name="comentarios_list_create",
    ),
    path(
        "temas/<int:pk>",
        apiviews.TemaForoDetail.as_view(),
        name="temas_detail",
    ),
    path(
        "comentarios/<int:pk>",
        apiviews.DetailUpdateComentariosPublicaciones.as_view(),
        name="comentarios_detail_update",
    ),
    path(
        "publicaciones/<int:pk>",
        apiviews.DetailUpdatePublicaciones.as_view(),
        name="posts_detail_update",
    ),
    path(
        "temas",
        apiviews.TemaForoList.as_view(),
        name="forum_topic_list",
    ),
    path(
        "destacados",
        apiviews.ListTopCommentsInPublicacion.as_view(),
        name="forum_destacados",
    ),
    path(
        "ultimos_comentarios",
        apiviews.ListPublicationsWithLastComments.as_view(),
        name="forum_ultimos_comentarios",
    ),
    path(
        "ultimos_hilos",
        apiviews.ListPublicationsRecents.as_view(),
        name="forum_ultimos_hilos",
    ),
    
]
