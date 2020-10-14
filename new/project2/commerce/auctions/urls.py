from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("auctions/", views.index, name="index"),
    path("auctions/login", views.login_view, name="login"),
    path("auctions/logout", views.logout_view, name="logout"),
    path("auctions/register", views.register, name="register"),
    path("auctions/watchlist", views.watchlist, name="watchlist"),
    path("auctions/categories", views.show_categories, name="categories"),
    path("auctions/create", views.create_listing, name="create"),
    path("auctions/<str:listing_name>", views.listing, name="listing"),
    path("auctions/categories/<str:category>/", views.category, name="category"),
    path("auctions/<str:listing_name>/comments/", views.show_comments, name="comments"),
    path("auctions/<str:listing_name>/comment/", views.comment, name="comment")
]
