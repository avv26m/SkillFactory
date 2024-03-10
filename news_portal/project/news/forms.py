from django import forms
from django.core.exceptions import ValidationError

from .models import NewsPost

class NewsForm(forms.ModelForm):
    Text = forms.CharField(min_length=20)
    class Meta:
        model = NewsPost
        fields = ['title','Text','category']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        Text = cleaned_data.get("Text")

        if title == Text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data