from django.shortcuts import render
from .models import Post
from django.http import Http404

# Create your views here.


def post_list(request):
    posts = Post.published_manager.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_details(request, year, month, day, post):
    try:
        post = Post.published_manager.get(
            slug=post, publish__year=year, publish__month=month, publish__day=day
        )
    except Post.DoesNotExist:
        return Http404

    return render(request, "blog/post/detail.html", {"post": post})
