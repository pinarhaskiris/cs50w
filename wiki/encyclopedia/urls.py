from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryName>", views.goToEntry, name="goToEntry"),
    path("search", views.search, name="search"),
    path("createNewPage", views.createNewPage, name="createNewPage"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("editPage/<str:entryName>", views.editPage, name="editPage")
]
