from django.conf.urls import url

from . import views

app_name = "posts"
urlpatterns = [
        url(r"^$", views.posts_list, name="index"),
        url(r"^add/?$", views.make_post, name="form"),
        url(r"^api/get_posts/?$", views.retrieve_posts, name="new_posts")
]
