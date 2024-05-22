from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage/", views.new_page, name="newpage"),
    path("search/", views.search, name="search"),
    path("edit/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("wiki/<str:title>", views.entry, name="entry")
]
