from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail

from .forms import EmailForm, CommentForm

from django.views.decorators.http import require_POST

from taggit import models as taggit_models

# Create your views here.


def post_list(request, tag_slug=None):
    posts = Post.published_manager.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(taggit_models.Tag, slug=tag_slug)
        posts = Post.published_manager.filter(tags__in=[tag])

    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"posts": posts, 'tag': tag})


def post_details(request, year, month, day, post):
    try:
        post = Post.published_manager.get(
            slug=post, publish__year=year, publish__month=month, publish__day=day
        )
    except Post.DoesNotExist:
        return Http404

    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


def post_share(request, post_id):
    post = Post.published_manager.get(id=post_id)
    sent = False
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            send_mail(
                f'{cleaned_data["name"]} recommends you read {post.title}',
                f"Read {post.title} at {post_url}",
                "nishant.nawarkhede@gmail.com",
                [cleaned_data["to"]],
                fail_silently=False,
            )
            sent = True
            # send email logic
    else:
        form = EmailForm()

    return render(
        request, "blog/post/share.html", {"form": form, "post": post, "sent": sent}
    )


@require_POST
def post_comment(request, post_id):
    try:
        post = Post.published_manager.get(id=post_id)
    except Post.DoesNotExist:
        return Http404

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"form": form, "comment": comment, "post": post},
    )
