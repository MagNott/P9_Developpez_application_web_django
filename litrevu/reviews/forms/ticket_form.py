from django import forms
from reviews.models.ticket_model import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'image': 'Image',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre du ticket', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description du ticket', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control btn btn-secondary'}),
        }