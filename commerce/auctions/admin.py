from django.contrib import admin
from .models import Category, Listing, User, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Bid)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'starting_bid')