from django.forms import ModelForm, Textarea
from .models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'review_title',
            'review_description',
        ]
        widgets = {
            'review_description': Textarea(attrs={'cols': 80, 'rows': 8}),
        }