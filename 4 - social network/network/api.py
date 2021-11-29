import json

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from . import views
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, User
from .views import index


@login_required
def like(request):
    # must be via POST
    if request.method != "POST" or request.body is None:
        return JsonResponse({"error": "POST request required."}, status=400)

    post_id = json.loads(request.body)["id"]

    if Post.objects.get(id=post_id).user.username == request.user.username:
        return JsonResponse({"error": "The user is liking his own post"})

    if Post.objects.filter(id=post_id, users_liking__username=request.user):
        Post.objects.get(id=post_id).users_liking.remove(request.user)
        return JsonResponse({"status": "success",
                             "op": "remove",
                             "like_count": len(Post.objects.get(id=post_id).users_liking.all())})
    else:
        Post.objects.get(id=post_id).users_liking.add(request.user)
        return JsonResponse({"status": "success",
                             "op": "add",
                             "like_count": len(Post.objects.get(id=post_id).users_liking.all())})


@login_required
def follow(request):

    # must be via POST
    if request.method != "POST" or request.body is None:
        return JsonResponse({"error": "POST request required."}, status=400)

    body = json.loads(request.body)

    username = body["username"]
    action = body["action"]

    if action == "Follow":
        request.user.following.add(User.objects.get(username=username))
        print("followed")
    elif action == "Unfollow":
        request.user.following.remove(User.objects.get(username=username))
        print("unfollowed")
    else:
        return JsonResponse({"error": "Bad action"}, status=404)

    return JsonResponse({"status": "OK"}, status=200)

@login_required
def edit(request):
    # must be via POST
    if request.method != "POST" or request.body is None:
        return JsonResponse({"error": "POST request required."}, status=400)
    body = json.loads(request.body)

    post_id = body.get("id")
    text = body.get("body")

    if len(text) <= 0:
        return JsonResponse({"error": "empty field"}, status=204)

    post = Post.objects.get(id=post_id)

    if post is None:
        return JsonResponse({"error": "Bad ID"}, status=404)

    if post.user != request.user:
        return JsonResponse({"error": "Bad Auth"}, status=404)

    post.body = text
    post.save()

    return JsonResponse(status=200, data={})


@login_required(redirect_field_name="login")
def new_post(request: HttpRequest):
    if request.POST:
        Post.objects.create(body=request.POST["body"], user=request.user)

    request.POST = None
    return redirect(index)
