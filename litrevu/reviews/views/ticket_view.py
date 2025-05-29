from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from reviews.models.ticket_model import Ticket
from reviews.forms.ticket_form import TicketForm


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket/ticket_create.html'
    title = 'Ajouter un Ticket'
    success_url = reverse_lazy('home')

    # Pour permettre d'associer la création a un utilisateur
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket/ticket_update.html'
    title = 'Modifier un Ticket'
    success_url = reverse_lazy('home')

    # Pour permettre d'associer la création a un utilisateur
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Empêche d’accéder aux tickets d’un autre utilisateur
    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'reviews/ticket/ticket_confirm_delete.html'
    success_url = reverse_lazy('home')

    # Empêche d’accéder aux tickets d’un autre utilisateur
    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
