from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment


CATEGORIES=[("toys","Toys"),
    ("furniture","Furniture"),
    ("electronics","Electronics"),
    ("clothing","Clothing"),
    ("decoration","Decoration"),
    ("other","Other")
]

class newListingForm(forms.Form):
    title = forms.CharField(label='Item Name', 
                    widget=forms.TextInput(attrs={'placeholder': 'Write your title here...', 'class': 'formInput'}))
    
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":10, 'placeholder': 'Write your description here...', 'class': 'formInput'}), label="Description")
    
    price = forms.IntegerField(label='Starting Bid', widget=forms.NumberInput(attrs={'class': 'formInput', 'placeholder': 'Write the starting price in US dollars here...'}))
    creationDate = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'required': 'required', 'class': 'formInput'}))
    
    imgUrl = forms.CharField(label='Img Url (optional)', required=False, 
                    widget=forms.TextInput(attrs={'class': 'formInput'}))


    category= forms.CharField(label='Category (optional)', widget=forms.Select(choices=CATEGORIES, attrs={'class': 'formInput'}))

class bidForm(forms.Form):
    bid = forms.IntegerField(label='Bid', widget=forms.NumberInput(attrs={'class': 'formInput'}))

class commentForm(forms.Form):
    comment = forms.CharField(label='Comment',
                    widget=forms.TextInput(attrs={'class': 'formInput'}))

def index(request):
    activeListings = Listing.objects.filter(isOpen=True)
    return render(request, "auctions/index.html", {
        "activeListings": activeListings 
        })

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

def createNewListing(request):
    if request.method == "POST":
        form = newListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            creationDate = form.cleaned_data["creationDate"]
            imgUrl = form.cleaned_data["imgUrl"]
            creator = request.user.username
            category = form.cleaned_data["category"][0]

            listItem = Listing.create_listing(title, description, price, creationDate, imgUrl, creator, category)
            listItem.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/createNewListing.html", {
                "form": form
                })

    return render(request, "auctions/createNewListing.html", {
        "form": newListingForm()
        })

def goToItem(request, itemTitle):
    itemObject = Listing.objects.filter(title=itemTitle).first()
    itemComments = Comment.objects.filter(listingName=itemTitle)
    itemTitle = itemObject.title
    itemDes = itemObject.description
    itemCreDate = itemObject.creationDate
    itemImg = itemObject.imgUrl
    itemWatch = itemObject.isWatchlisted
    itemCreator = itemObject.creator
    isItemOpen = itemObject.isOpen
    itemCategory = itemObject.category

    return render(request, "auctions/goToItem.html", {
        "itemTitle": itemTitle,
        "itemDes": itemDes,
        "itemImg": itemImg,
        "itemPrice": highestBid(itemTitle)[0],
        "highestBidder": highestBid(itemTitle)[1],
        "itemCreDate": itemCreDate,
        "itemWatch": itemWatch,
        "form": bidForm(),
        "itemCreator": itemCreator,
        "isItemOpen": isItemOpen,
        "commentForm": commentForm(),
        "itemComments": itemComments,
        "itemCategory": itemCategory
        })

def showWatchlist(request):
    watchlist = Listing.objects.filter(isWatchlisted=True)
    return render(request, "auctions/showWatchlist.html", {
        "watchlist": watchlist
        })

def addToWatchlist(request, itemTitle):
    Listing.objects.filter(title=itemTitle).update(isWatchlisted=True)
    watchlist = Listing.objects.filter(isWatchlisted=True)
    return render(request, "auctions/showWatchlist.html", {
        "watchlist": watchlist
        })

def removeFromWatchlist(request, itemTitle):
    Listing.objects.filter(title=itemTitle).update(isWatchlisted=False)
    watchlist = Listing.objects.filter(isWatchlisted=True)
    return render(request, "auctions/showWatchlist.html", {
        "watchlist": watchlist
        })

def bid(request, itemTitle):
    if request.method == "POST":
        form = bidForm(request.POST)
        if form.is_valid():
            username = request.user.username
            bid = form.cleaned_data["bid"]

            if  Listing.objects.filter(title=itemTitle).first().isOpen:

                if bid < Listing.objects.filter(title=itemTitle).first().price:
                    return render(request, "auctions/invalidBid.html", {
                        "itemTitle": itemTitle
                        })
                else:

                    bidItem = Bid.create_bid(username, bid, itemTitle)
                    bidItem.save()
            else:
                return render(request, "auctions/closedListing.html", {
                    "itemTitle": itemTitle
                    })

            return HttpResponseRedirect(reverse("goToItem", args=[itemTitle]))
        else:
            return HttpResponseRedirect(reverse("goToItem", args=[itemTitle]))

    return HttpResponseRedirect(reverse("index"))

def comment(request, itemTitle):
    if request.method == "POST":
        comForm = commentForm(request.POST)
        if comForm.is_valid():
            username = request.user.username
            comment = comForm.cleaned_data["comment"]

            commentItem = Comment.create_comment(username, comment, itemTitle)
            commentItem.save()

            return HttpResponseRedirect(reverse("goToItem", args=[itemTitle]))
        else:
            return HttpResponseRedirect(reverse("goToItem", args=[itemTitle]))

    return HttpResponseRedirect(reverse("index"))


def highestBid(itemTitle):
    bids = Bid.objects.filter(bidItem=itemTitle).values('bid')
    highestBid = Listing.objects.filter(title=itemTitle).first().price

    if not bids:
        return Listing.objects.filter(title=itemTitle).first().price, Listing.objects.filter(title=itemTitle).first().creator

    for bid in bids:
        if bid["bid"] > highestBid:
            highestBid = bid["bid"]

    #update the current price & select the highest bidder
    Listing.objects.filter(title=itemTitle).update(price=highestBid)
    highestBidder = Bid.objects.filter(bid=highestBid).first().bidder

    return highestBid, highestBidder

def closeListing(request, itemTitle):
    #close listing to more bids
    bidItem = Listing.objects.filter(title=itemTitle).first()
    bidItem.isOpen = False
    bidItem.save()

    return HttpResponseRedirect(reverse("goToItem", args=[itemTitle]))

def categories(request):
    categoryNames = [ i[0] for i in CATEGORIES ]
    return render(request, "auctions/categories.html", {
        "categories": categoryNames
        })

def goToCategory(request, categoryName):
    categoryListings = Listing.objects.filter(category=categoryName)
    return render(request, "auctions/goToCategory.html", {
        "categoryName": categoryName,
        "categoryListings": categoryListings
        })





