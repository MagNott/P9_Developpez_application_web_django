from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nom d’utilisateur',
            'class': 'form-control mb-4',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Mot de passe',
            'class': 'form-control mb-4',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirmez le mot de passe',
            'class': 'form-control',
        })


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nom d’utilisateur',
            'class': 'form-control mb-4',
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Mot de passe',
            'class': 'form-control',
        })
