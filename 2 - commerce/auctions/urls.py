from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:id_listing>", views.show_listing, name="show_listing"),
    path("listing/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.show_watchlist, name="show_watchlist"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("listing/remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("new_listing", views.new_listing, name="new listing"),
    path("past_listings", views.past_listings, name="past_listings"),
    path("categories", views.show_categories, name="categories"),
    path("random", views.random, name="random")

]

