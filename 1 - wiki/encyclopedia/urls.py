from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), #path is an empty string, so there is nothing at the end of the URL, VIEWS.INDEX IS THE NAME OF THE FUNCTION THAT IS CALLED, and name= is an ID
    path("wiki/<str:wiki_name>", views.render_wiki, name="renderWiki"),
    path("edit", views.edit_entry, name="edit_entry"),
    path("random", views.view_random_entry, name="random"),
    path("search/", views.search, name="searchEntry"),
    path("new", views.add_entry, name="new")
]
