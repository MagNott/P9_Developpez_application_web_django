from django import forms
from reviews.models.review_model import Review


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
      (0, '0'),
      (1, '1'),
      (2, '2'),
      (3, '3'),
      (4, '4'),
      (5, '5'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Note"
    )

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Titre', 'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }