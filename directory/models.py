from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    following = models.BooleanField()
    location = models.CharField(max_length=254, unique=True)
    ip = models.GenericIPAddressField()
    last_updated = models.DateTimeField()
    cert = models.TextField()
    verified = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "people"
