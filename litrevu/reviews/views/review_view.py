from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from reviews.models.ticket_model import Ticket
from reviews.models.review_model import Review
from reviews.forms.review_form import ReviewForm


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review/review_create.html'
    title = 'Ajouter une critique'
    success_url = reverse_lazy('home')

    # Pour permettre d'associer la création a un utilisateur
    def form_valid(self, form):
        form.instance.user = self.request.user
        ticket_id = self.kwargs['ticket_id']  # récupère depuis l’URL
        form.instance.ticket_id = ticket_id
        return super().form_valid(form)

    # Apporter du contexte pour avoir les infos concernant le ticket correspondant
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs['ticket_id']
        ticket = Ticket.objects.get(id=ticket_id)
        context['ticket'] = ticket
        return context


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review/review_update.html'
    title = 'Modifier une critique'
    success_url = reverse_lazy('home')

    # Pour permettre d'associer la création a un utilisateur
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Empêche d’accéder aux tickets d’un autre utilisateur
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    # Apporter du contexte pour avoir les infos concernant le ticket correspondant
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.object.ticket
        context['ticket'] = ticket
        return context


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review/review_confirm_delete.html'
    success_url = reverse_lazy('home')

    # Empêche d’accéder aux tickets d’un autre utilisateur
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    # Apporter du contexte pour avoir les infos concernant le ticket correspondant
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.object.ticket
        context['ticket'] = ticket
        return context
