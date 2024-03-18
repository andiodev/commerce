from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.addlisting, name="add_listing"),
    path("choose_category", views.chooseCategory, name="choose_category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("add_watch_list/<int:id>", views.addWatchList, name="add_watch_list"),
    path("remove_watch_list/<int:id>", views.removeWatchList, name="remove_watch_list"),
    path("watch_list", views.watchList, name="watch_list"),
    path("add_comment/<int:id>", views.addComment, name="add_comment"),
    path("add_bid/<int:id>", views.addBid, name="add_bid"),
    path("close_auction/<int:id>", views.closeAuction, name="close_auction"),
]
