
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("network", views.network, name="network"),
    path("profile", views.profile, name="profile"),
    path("editpost", views.editpost, name="editpost"),
    path("following", views.following, name="following")
]
