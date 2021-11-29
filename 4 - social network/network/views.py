from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse

from django.core.paginator import Paginator

from .models import User, Post, Comment


def index(request):
    return page(request, 1)


def page(request, page_num):
    if not request.user.is_authenticated:
        page_num = 1

    posts = Paginator(Post.objects.all().order_by("-date"), 10)

    if page_num > posts.num_pages or page_num < 1:
        page_num = 1

    context = {
        "posts": posts.page(page_num),
    }

    return render(request, "network/index.html", context)


def user(request, username):
    if username is None:
        return HttpResponseServerError(404)

    user = None

    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponseServerError(404)

    follow_status = "Follow"

    if request.user.is_authenticated:
        if User.objects.get(id=request.user.id).following.filter(username=username):
            follow_status = "Unfollow"


    context = {
        "userp": user,
        "follower_count": len(User.objects.filter(following__username=username)),
        "following_count": len(user.following.all()),
        "follow_status": follow_status,
        "posts": Post.objects.filter(user__username__exact=username).order_by("-date")
    }

    return render(request, "network/profile.html", context)


@login_required
def following(request):
    return following_page(request, 1)


@login_required
def following_page(request, page_num):
    posts = Post.objects.filter(user__in=User.objects.get(id=request.user.id).following.all()).order_by("-date")

    pages = Paginator(posts, 10)

    if page_num > pages.num_pages or page_num < 1:
        page_num = 1

    if pages.num_pages < 1:
        return HttpResponse("Yo follow someone")

    context = {
        "posts": pages.page(page_num)
    }

    return render(request, "network/index.html", context)


def comments(request):
    context = {}

    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))

    post = Post.objects.get(id=request.POST.get("post_id"))

    if post is None:
        return HttpResponseServerError(500)

    if request.POST:
        post_id = request.POST.get("post_id")

        if request.POST.get("new_comment") is not None and request.user.is_authenticated:
            Comment.objects.create(body=request.POST.get("new_comment"), post_id=post_id, user=request.user)

        if request.POST.get("body"):
            post = Post.objects.get(id=post_id)
            post.body = request.POST.get("body")
            post.save()

        context = {
            "post": post,
            "comments": Comment.objects.filter(post_id=post_id)
        }
    else:
        return reverse("index")

    return render(request, "network/comment.html", context)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
