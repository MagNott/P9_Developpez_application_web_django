from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('home')  # à adapter selon ta logique

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # connecte automatiquement l'utilisateur
        return response