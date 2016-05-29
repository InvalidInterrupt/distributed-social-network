from django.conf.urls import url

from . import views

app_name = "directory"
urlpatterns = [
        url(r"^$", views.index, name="index"),
        url(r"^add/?$", views.add, name="add"),
        url(r"^self/info/?$", views.get_info, name="info")
]
