from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User
from .models import Item
from .models import Category
from .models import Comment
from .models import Bid

from .forms import NewBidForm, NewCategoryForm, NewItemForm, NewCommentForm
from .util import get_max_bid
from . import util
from datetime import date

from random import randint
def index(request):
    context = {
        "header": "Active Listings",
        "listings": Item.objects.filter(is_active=True)
    }
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


def show_listing(request, id_listing):
    listing = Item.objects.get(id=id_listing)
    form = NewBidForm(request.POST, item_id=id_listing)

    bids = Bid.objects.filter(item_id=id_listing).order_by("-ammount")

    comment_form = NewCommentForm(request.POST or None)

    comment_form.fields.get("comment").widget.attrs.update({"required": False})

    context = {
        "listing": listing,
        "categories": listing.categories.all(),
        "comments": Comment.objects.filter(item_id=id_listing),
        "in_watchlist": util.is_in_watchlist(request.user, listing),
        "user_is_owner": listing.owner == request.user,
        "user_is_winner": len(bids) > 0 and request.user.id is bids.first().bidder.id,
        "item_is_active": listing.is_active,
        "max_bid": util.get_max_bid(id_listing),
        "bids": bids,
        "bids_len": len(bids),
        "comment_form": comment_form,
    }

    form.fields.get("ammount").widget.attrs.update({"min": get_max_bid(id_listing) + 0.01})

    context.update({"form": form})

    if request.POST:
        print(request.POST)

        if request.POST.get("bid") and form.is_valid() :
            model_form = form.save(commit=False)
            try:
                model_form.bidder = request.user
                model_form.item = Item.objects.get(id=id_listing)
                model_form.save()
                context.update({"max_bid": request.POST.get("ammount")})
                return render(request, "auctions/listing.html", context)
            except KeyError:
                return HttpResponseNotFound("User or item not found")

        else:
            context.update({"form_error": True})

        if request.POST.get("comment") and comment_form.is_valid():
            save_form = comment_form.save(commit=False)
            save_form.user = request.user
            save_form.save()


    return render(request, "auctions/listing.html", context)


@login_required(login_url="/login")
def add_watchlist(request):
    if request.POST:
        user = request.user
        item: int = request.POST.get("item")

        if Item.objects.get(id=item):
            # guardar la wea
            Item.objects.get(id=item).users_watching.add(user)

            return HttpResponseRedirect(reverse("show_listing", kwargs={"id_listing": item}))
    return HttpResponseNotFound(f"Item does not exist")


@login_required(login_url="/login")
def show_watchlist(request):
    if request.user is None:
        return HttpResponseNotFound(f"User {request.user} not found")

    listing = util.obtain_watchlist(request.user)

    context = {"header": "My Watchlist",
               "listings": listing,
               }

    return render(request, "auctions/index.html", context)


@login_required(login_url="login")
def close_auction(request):
    if request.POST:
        item = Item.objects.get(id=request.POST.get("item_close"))
        if item is None:
            return HttpResponseNotFound("Item not found")
        else:
            if item.owner.id is not request.user.id:
                return HttpResponse("You are not the owner of this item")
            else:
                item.is_active = False
                item.save()
                return show_listing(request, item.id)

    return None


@login_required(login_url="/login")
def remove_watchlist(request):
    if request.POST:
        user = request.user
        item: int = request.POST.get("item")

        if Item.objects.get(id=item):
            # guardar la wea
            Item.objects.get(id=item).users_watching.remove(user)

            return HttpResponseRedirect(reverse("show_listing", kwargs={"id_listing": item}))
        else:
            return HttpResponse("You are not the owner of the item")

    return HttpResponseNotFound(f"Item does not exist")


@login_required(login_url="/login")
def new_listing(request):
    form = NewItemForm(request.POST or None)
    form_cat = NewCategoryForm(request.POST or None)
    form_cat.fields.get("name").widget.attrs.update({"required": False})
    context = {
        "form": form,
        "cat_form": form_cat
    }

    form.fields.get("item_name").widget.attrs.update({"min_length": 3})
    context.update({"form": form})

    if request.POST:

        if request.POST.get("new_cat") and form_cat.is_valid():
            form_cat.save()
            return render(request, "auctions/new_listing.html", context)

        if request.POST.get("submit") and form.is_valid():
            if (request.POST.get("submit")):
                form_model = form.save(commit=False)
                form_model.owner = request.user
                form_model.item_description = form.cleaned_data.get("item_description")
                form_model.is_active = True
                form_model.date = date.today()
                form_model.save()
                form.save_m2m()
                return show_listing(request, form_model.id)

    return render(request, "auctions/new_listing.html", context)


def past_listings(request):
    context = {
        "header": "Past / Inactive Listings",
        "listings": Item.objects.filter(is_active=False)
    }
    return render(request, "auctions/index.html", context)


def show_categories(request):
    context = {"categories": Category.objects.all().order_by("name")}
    if request.GET:
        items_category = Item.objects.filter(categories=request.GET.get("value"))
        context_list = {
            "header": f"{request.GET.get('value')} items",
            "listings": items_category
        }
        return render(request, "auctions/index.html", context_list)


    return render(request, "auctions/show_categories.html", context)

def random(request):
    items = Item.objects.all()
    id_listing = randint(0, len(items)-1 )
    return show_listing(request,list(items).__getitem__(id_listing).id)