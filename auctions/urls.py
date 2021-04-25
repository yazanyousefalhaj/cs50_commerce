from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/create", views.create_auction, name="create_auction"),
    path("auction/<int:auction_id>/edit", views.edit_auction, name="edit_auction"),
    path("auction/<int:auction_id>", views.auction_index, name="auction_index"),
    path("auction/<int:auction_id>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("auction/<int:auction_id>/remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("auction/<int:auction_id>/close_auction", views.close_auction, name="close_auction"),
    path("auction/<int:auction_id>/create_bid", views.create_bid, name="create_bid"),
    path("auction/<int:auction_id>/create_comment", views.create_comment, name="create_comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>/auctions", views.category_auctions, name="category_auctions"),


]
