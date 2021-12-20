import os
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls import include, url
from userprofile import apiviews


urlpatterns = [
    path(
        "<int:pk>",
        apiviews.UserDetail.as_view(),
        name="user_detail",
    ),
    path(
        "search/",
        apiviews.UserSearch.as_view(),
        name="user_search",
    ),
    path(
        "perfil/<int:pk>",
        apiviews.UserNonDiscriteDetailUpdate.as_view(),
        name="user_profile_detail_update",
    ),
    path(
        "registro",
        apiviews.UserCreate.as_view(),
        name="user_register",
    ),
    path(
        "<int:pk>/avatar",
        apiviews.AvatarDetail.as_view(),
        name="avatar_detail",
    ),
    path(
        "recover_pass",
        apiviews.PaswordRecover.as_view(),
        name="recover_pass",
    ),
    path(
        "pass_reset",
        apiviews.PaswordChange.as_view(),
        name="pass_reset",
    ),
    path("api-token-auth/", apiviews.CustomAuthToken.as_view(), name="auth-login"),
]
