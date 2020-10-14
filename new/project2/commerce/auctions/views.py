from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .login_required import login_required

import pdb

from .models import *

def index(request):
    if request.method == "POST":
        name = request.POST["listing"]
        description = request.POST["description"]
        price = float(request.POST["price"])
        url = request.POST["inputurl"]
        category = request.POST["category"]
        date = timezone.now()
        username = request.user 
        listing = AuctionListings(name = name, user_name = username, count_bids = 0, price = price, 
            description = description, image_url = url, created_date = date, actual = True)
        listing.save()
        listing.categories_set.create(category = category)

    print(213)
    listings = AuctionListings.objects.filter(actual = True)
    context = {'listings': listings}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def load_listing(request, listing_name):
    listing = AuctionListings.objects.get(name = listing_name)
    category = listing.categories_set.get().category
    count_watchlists = listing.watchlists_set.filter(user=request.user).count()
    context = {
        'listing': listing,
        'count': count_watchlists,
        'category': category
    }
    return render(request, "auctions/listing.html", context)

@login_required
def listing(request, listing_name):

    if request.method == "POST":
        if "bid" in request.POST:
            bid_price = request.POST["bid"]
            username = request.user
            date = timezone.now()
            listing = AuctionListings.objects.get(name=listing_name)
            listing.auctionbids_set.create(bid_price=bid_price, user_bid=username, date=date)
            listing.count_bids += 1
            listing.save()
            return load_listing(request, listing_name)
        else:
            username = request.user
            listing = AuctionListings.objects.get(name=listing_name)
            listing.watchlists_set.create(user=username)
            return load_listing(request, listing_name)

    else: return load_listing(request, listing_name)

@login_required
def watchlist(request):
    username = request.user
    watches = Watchlists.objects.filter(user=username)
    context = {'listings': watches}
    # pdb.set_trace()
    return render(request, "auctions/watchlist.html", context)

@login_required
def create_listing(request):
    categories = ["sport", "beayti", "music", "art", "house", "kitchen", "other"]
    context = {'categories': categories}
    return render(request, "auctions/create.html", context)

def show_categories(request):
    categories = ["sport", "beayti", "music", "art", "house", "kitchen", "other"]
    context = {'categories': categories}
    return render(request, "auctions/categories.html", context)

def category(request, category):
    listings = Categories.objects.filter(category = category)
    context = {'listings': listings}
    return render(request, "auctions/category.html", context)

@login_required
def comment(request, listing_name):
    context = {'listing': listing_name}
    return render(request, "auctions/comment.html", context)

@login_required
def show_comments(request, listing_name):

    if request.method == "POST":
        comment_text = request.POST["addcomment"]
        user = request.user
        date = timezone.now()
        listing = AuctionListings.objects.get(name=listing_name)
        listing.auctioncomments_set.create(comment_text=comment_text,user=user,date=date)

    listing = AuctionListings.objects.get(name=listing_name)
    comments = listing.auctioncomments_set.all()
    context = {
        'comments': comments,
        'listing': listing_name
    }
    return render(request, "auctions/comments.html", context)