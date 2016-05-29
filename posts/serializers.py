from rest_framework import serializers

from .models import Post

class RecipientPostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="location",
                                          read_only=True)
    class Meta:
        model = Post
        fields = ("author", "content", "created", "last_modified")
