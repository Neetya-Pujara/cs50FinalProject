from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("new_page", views.new_page, name="new_page"),
    path("random", views.random, name="random"),
    path("<str:title>/edit", views.edit_page, name="edit_page"),
    path("<str:title>", views.topic, name="topic")
]
