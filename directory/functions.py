from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from ecdsa import BadSignatureError, VerifyingKey
from hashlib import sha256
import socket
import ssl

from .models import Person

def auth_person_ssl(func):
    def new_func(request):
        if request.META.get("nginx.ssl_client_raw_cert"):
            cert = load_pem_x509_certificate(request.META["SSL_CLIENT_CERT"])
            if cert:
                try:
                    person = Person.objects.get(location=cert.subject)
                except Person.DoesNotExist:
                    return func(request, None)
                expected_cert = load_pem_x509_client_certificate(person.cert)
                if expceted_cert == cert:
                    return func(request, person)
                else:
                    return HttpResponseForbidden()
        return func(request, None)
    return new_func

def verify_signature(content, signature, signing_person):
    backend = default_backend()
    cert = load_pem_x509_certificate(signing_person.cert, backend)
    key = cert.public_key()
    try:
        key.verify(signature, content, hashfunc=sha256)
    except BadSignatureError:
        return False
    else:
        return True

def resolve_location(person):
    location = person.location
    email = "@" in location
    if not email:
        return location
    else:
        raise Exception("Not implemented")
