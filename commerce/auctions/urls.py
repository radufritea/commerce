from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.listings, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<int:pk>", views.listing, name="listing_details"),
    path("categories", views.CategoriesListView.as_view(), name="categories"),
    path("category/<int:pk>", views.category_listings, name="category"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("watch_manager", views.watch_manager, name="watch_manager"),
    path("bid", views.bid, name="bid"),
    path("comment", views.add_comment, name="add_comment"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)