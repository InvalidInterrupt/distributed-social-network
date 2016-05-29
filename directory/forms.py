from django import forms

from .models import Person

class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["location", "following"]

    def clean_location(self):
        location = self.cleaned_data.get("location")
        if location and "@" in location:
            raise forms.ValidationError("Emial location nto yet supported")
        return location
