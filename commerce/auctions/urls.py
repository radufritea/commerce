from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.ListingsListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<int:pk>", views.ListingDetailsView.as_view(), name="listing_details"),
    path("categories", views.CategoriesListView.as_view(), name="categories"),
    path("category/<int:pk>", views.category_listings, name="category"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("watch_manager", views.watch_manager, name="watch_manager"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)