import django
import os
import sys
import threading

def setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dsn.settings")
    django.setup()
    from .models import Agent
    return Agent.objects.first()

def update_looper(agent):
    for person in Person.objects.filter(following=True, agent=None):
        get_updates(person, agent)
    threading.Timer(300, update_looper, args=[agent]).start()

if __name__ == "__main__":
    agent = setup()

    from directory.models import Person
    from posts.functions import get_updates

    threading.Timer(300, update_looper, args=[agent]).start()
