from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createNewListing", views.createNewListing, name="createNewListing"),
    path("/<str:itemTitle>", views.goToItem, name="goToItem"),
    path("showWatchlist", views.showWatchlist, name="showWatchlist"),
    path("addToWatchlist/<str:itemTitle>", views.addToWatchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<str:itemTitle>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("bid/<str:itemTitle>", views.bid, name="bid"),
    path("closeListing/<str:itemTitle>", views.closeListing, name="closeListing"),
    path("comment/<str:itemTitle>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("goToCategory/<str:categoryName>", views.goToCategory, name="goToCategory")
]
