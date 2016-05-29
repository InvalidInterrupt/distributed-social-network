from rest_framework import serializers

from .models import Person

class PublicPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("name", "location", "cert")
