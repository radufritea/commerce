from multiprocessing import AuthenticationError
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Category, User, Listing, Watchlist, Bid, Comment
from .forms import ListingForm

# Create a new listing
def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ListingForm()
    
    return render(request, "auctions/add_listing.html", {"form": form})


# LISTING DETAIL
def listing(request, pk):
    listing = Listing.objects.get(id=pk)
    comments = Comment.objects.filter(listing_id=pk)
    return render(request, 'auctions/listing_detail.html', {
        'listing': listing,
        "comments": comments,
    })


# INDEX - all listings
def listings(request):
    listings = Listing.objects.all()
    return render(request, 'auctions/index.html', {
        'listings': listings
    })


class CategoriesListView(ListView):
    model = Category


# List all listings in a certain category
def category_listings(request, pk):
    listings = Listing.objects.filter(category=pk)
    category = Category.objects.get(pk=pk)
    return render(request, "auctions/category.html", {"listings": listings, "category": category})


# Show user's watchlist
@login_required
def show_watchlist(request):
    current_user = request.user
    watchlist = current_user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"watchlist": watchlist})


# Add or remove a listing from the watchlist
@login_required
def watch_manager(request):
    pk = request.GET.get('pk')
    watchlist = Watchlist.objects.all()
    print(pk)
    listing = Listing.objects.get(id=pk)
# save listing as a list so you can iterate through it
    if listing in watchlist:
        Watchlist.objects.filter(listing_id=pk).delete()
    else:
        Watchlist.objects.create(user_id=request.user.id, listing_id=pk)

    return redirect("listing_details", pk)


# Make a bid if conditions are met
@login_required
def bid(request):
    if request.method == "POST":
        bid_value = int(request.POST.get("bid_value"))
        pk = request.GET.get('pk')
        listing = Listing.objects.get(id=pk)
        current_bid = Bid.objects.filter(listing=pk, value__gt=bid_value)
        message = ""

        if bid_value < listing.starting_bid:
            message = "Your bid is smaller than the starting bid."
            
        elif not current_bid:
            Bid.objects.create(value=bid_value, listing_id=listing.id, user_id=request.user.id)
            message = "Your bid has been recorded."

        else:
            # error your bid is smaller
            message = "Your bid is smaller than the largest existing bid."

        print(message)
        return redirect ("listing_details", pk)

@login_required
def add_comment(request):
    if request.method == "POST":
        pk = request.GET.get('pk')
        text = request.POST.get("comment_text")
        listing = Listing.objects.get(id=pk)
        Comment.objects.create(author_id=request.user.id, listing_id=listing.id, text=text)
    
    return redirect ("listing_details", pk)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")