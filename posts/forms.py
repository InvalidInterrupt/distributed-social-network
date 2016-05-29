from django import forms
from django.utils.timezone import now

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]

class PastTimeForm(forms.Form):
    time = forms.DateTimeField()

    def clean_time(self):
        time = self.cleaned_data.get("time")
        if time > now():
            raise forms.ValidationError("In the future", code="future")
        else:
            return time
