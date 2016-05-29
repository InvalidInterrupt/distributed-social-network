import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import activate, now
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import PastTimeForm, PostForm
from .models import Post
from .serializers import RecipientPostSerializer
from agent.models import Agent
from directory.functions import auth_person_ssl
from directory.models import Person


@login_required
def posts_list(request):
    posts = Post.objects.filter(deleted=False).order_by("-created")
    context = {
            "title": "Posts",
            "section": "posts",
            "posts": posts
    }
    return render(request, "posts_list.html", context)

@login_required
def make_post(request):
    time = now()
    instance = Post(author=request.user.agent_set.get().person,
                    created=time, last_modified=time,
                    deleted=False)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse(
                "posts:index",
                current_app=request.resolver_match.namespace))
    context = {
            "title": "Write a post",
            "section": "posts",
            "form": form
    }
    return render(request, "posts_form.html", context)

@api_view(("GET",))
@auth_person_ssl
def retrieve_posts(request, person):
    activate("utc")
    form = PastTimeForm(request.query_params or None)
    if form.is_valid():
        filters = {"author": Agent.objects.get().person, "deleted": False,
                   "last_modified__gte": form.cleaned_data["time"]
                  }
        posts = Post.objects.filter(shared_with=None, **filters)
        if person:
            posts = posts | person.shared_post_set.filter(**filters)
        serializer = RecipientPostSerializer(posts, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response(form.errors, status=400)
