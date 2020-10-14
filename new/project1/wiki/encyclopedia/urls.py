from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_name>/", views.show_page, name="entry"),
    path("create_page/", views.create_page, name="create"),
    path("wiki/<str:page_name>/edit/", views.edit_page, name="edit"),
    path("random_page/", views.random_page, name="random"),
    path("search/", views.search_page, name="search")
]
