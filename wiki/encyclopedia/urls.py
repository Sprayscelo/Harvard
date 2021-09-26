from django.urls import path
from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:linguage>", views.pages, name="pages" ),
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("edit<str:entry>/", views.edit, name="edit"),
    path("random/", views.ran, name="random")
]