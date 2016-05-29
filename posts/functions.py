from datetime import timedelta
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from rest_framework.parsers import JSONParser
import ssl
import tempfile
import urllib.parse
import urllib.request

from directory.functions import resolve_location
from directory.models import Person
from posts.serializers import RecipientPostSerializer

def get_updates(person, agent):
    started = now()
    with tempfile.NamedTemporaryFile() as key_file:
        #TODO: encrypt on disk
        key_file.write(agent.private_key.encode())
        key_file.flush()
        with tempfile.NamedTemporaryFile() as cert_file:
            cert_file.write(agent.person.cert.encode())
            cert_file.flush()
            ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,
                                                     cadata=person.cert)
            ssl_context.load_cert_chain(cert_file.name, key_file.name)
            host = resolve_location(person)
            query = [("time", person.last_updated.strftime("%Y-%m-%d %H:%M:%S"))]
            query = urllib.parse.urlencode(query)
            url = urllib.parse.urlunparse(("https", ":".join((host, "8080")),
                                           reverse("posts:new_posts"), "",
                                           query, ""))
            response = urllib.request.urlopen(url, context=ssl_context)
    if response.status != 200:
        raise Exception(
                "Failed to retireve new posts for {0} <{1}>".format(
                    person.name, person.location)
                )
    data = JSONParser().parse(response)
    serializer = RecipientPostSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save(deleted=False, author=person)
        person.last_updated = started - timedelta(seconds=5)
        person.save()
    else:
        raise Exception("Invalid data from {0} <{1}>".format(
                person.name, person.location))
