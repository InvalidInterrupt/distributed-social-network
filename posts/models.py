from django.db import models

from directory.models import Person

class Post(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField()
    last_modified = models.DateTimeField()
    shared_with = models.ManyToManyField(Person,
                                         related_name="shared_post_set")
    deleted = models.BooleanField()
