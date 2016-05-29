import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from http.client import HTTPSConnection
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import ssl

from .forms import AddPersonForm
from .functions import resolve_location
from .models import Person
from .serializers import PublicPersonSerializer
from agent.models import Agent

@login_required
def index(request):
    people = Person.objects.filter(agent=None)
    context = {"people": people, "section": "directory"}
    return render(request, "people.html", context)

@login_required
def add(request):
    instance = Person(verified=False, ip="127.0.0.1",
                      last_updated=datetime.datetime.utcfromtimestamp(0))
    form = AddPersonForm(request.POST or None, instance=instance)
    if form.is_valid():
        person = form.save(commit=False)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        host = resolve_location(person)
        connection = HTTPSConnection(host=host, port=8080,
                                     context=ssl_context)
        connection.request("GET", reverse("directory:info"))
        response = connection.getresponse()
        data = JSONParser().parse(response)
        cert  = connection.sock.getpeercert()
        connection.close()
        serializer = PublicPersonSerializer(person, data=data)
        cn = None
        #for key, value in cert["subject"]:
        #    if key == "commonName":
        #        cn = value
        #        break
        #if cn == person.location and serializer.is_valid():
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse("directory:index"))
    context = {"form": form, "section": "directory"}
    return render(request, "person_form.html", context)

@api_view(("GET",))
def get_info(request):
    myself = Agent.objects.first().person
    serializer = PublicPersonSerializer(myself)
    return Response(serializer.data)
