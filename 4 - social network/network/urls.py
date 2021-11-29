
from django.urls import path

from . import views
from . import api

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page_num>", views.page, name="page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("comments", views.comments, name="comments"),
    path("following", views.following, name="following"),
    path("following/<int:page_num>", views.following_page, name="following_page"),
    path("user/<str:username>", views.user, name="user"),

    path("api/like", api.like, name="api_like"),
    path("api/newPost", api.new_post, name="api_new_post"),
    path("api/edit", api.edit, name="api_edit"),
    path("api/follow", api.follow, name="api_follow")
]
