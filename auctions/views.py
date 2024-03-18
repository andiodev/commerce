from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comments, Bid


def index(request):
    active_listings = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listing_data": active_listings,
        "categories": categories
    })

def chooseCategory(request):

    if request.method == "POST" and request.POST['category'] != 'None':
        select_category = request.POST['category']
        get_category = Category.objects.get(name=select_category)
        active_listings = Listing.objects.filter(active=True, category=get_category)
        categories = Category.objects.all()
        return render(request, "auctions/category.html",{
            "listing_data": active_listings,
            "categories": categories
        })
    else:
        categories = Category.objects.all()
        return render(request, "auctions/category.html",{
            "listing_data": None,
            "categories": categories
        })

def listing(request,id):
    listing = Listing.objects.get(id=id)
    isListingWL = request.user in listing.watch_listing.all()
    all_comment = Comments.objects.filter(listing=listing)
    is_owner = request.user.username == listing.owner.username
    return render(request, "auctions/listing.html",{
        "listing": listing,
        "isListingWL": isListingWL,
        "comments": all_comment,
        "isOwner": is_owner
    })

def closeAuction(request, id):
    data = Listing.objects.get(id=id)
    data.active = False
    data.save()
    isListingWL = request.user in data.watch_listing.all()
    all_comment = Comments.objects.filter(listing=data)
    is_owner = request.user.username == data.owner.username
    return render(request, "auctions/listing.html",{
        "listing": data,
        "isListingWL": isListingWL,
        "comments": all_comment,
        "isOwner": is_owner,
        "result": 200
    })

def addlisting(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/add_listing.html",{
            "categories": categories
        })
    else:
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST['imageUrl']
        price = request.POST['price']
        category = request.POST['category']
        user = request.user
        bid = Bid(bid=int(price), user=user)
        bid.save()

        get_category = Category.objects.get(name=category)
        add = Listing(
            title = title,
            description = description,
            image_url = image_url,
            starting_bid = bid,
            owner = user,
            category = get_category
        )

        add.save()
        return HttpResponseRedirect(reverse(index))

def addBid(request, id):
    new_bid = request.POST['new_bid']
    data = Listing.objects.get(id=id)
    isListingWL = request.user in data.watch_listing.all()
    all_comment = Comments.objects.filter(listing=data)
    is_owner = request.user.username == data.owner.username
    if int(new_bid) > data.starting_bid.bid:
        update_bid = Bid(user=request.user, bid=int(new_bid))
        update_bid.save()
        data.starting_bid = update_bid
        data.save()
        return render(request, 'auctions/listing.html',{
            "listing": data,
            "result": 200,
            "isListingWL": isListingWL,
            "comments": all_comment,
            "isOwner": is_owner,
        })
    else:
        return render(request, 'auctions/listing.html',{
            "listing": data,
            "result": 500,
            "isListingWL": isListingWL,
            "comments": all_comment,
            "isOwner": is_owner,
        })

def watchList(request):
    user = request.user
    listings = user.watch_listing.all()
    return render(request, 'auctions/watchlist.html',{
        "listing_data": listings
    })

def addWatchList(request, id):
    listing_data = Listing.objects.get(id=id)
    listing_data.watch_listing.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def removeWatchList(request, id):
    listing_data = Listing.objects.get(id=id)
    listing_data.watch_listing.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def addComment(request, id):
    user = request.user
    data = Listing.objects.get(id=id)
    message = request.POST['new_comment']

    new = Comments(
        author = user,
        listing = data,
        message = message
    )

    new.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

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
