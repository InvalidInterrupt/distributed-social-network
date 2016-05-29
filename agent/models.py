from django.conf import settings
from django.db import models

from directory.models import Person


class Agent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    person = models.ForeignKey(Person)
    private_key = models.TextField()

    def __str__(self):
        return "{0}'s Agent".format(self.person.name)
