from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from reviews.models.ticket_model import Ticket
from reviews.models.review_model import Review
from reviews.forms.review_form import ReviewForm
from django.http import HttpResponse
from typing import Any, Dict
from django.db.models import QuerySet


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Vue permettant à un utilisateur authentifié de créer une critique (Review)
    associée à un ticket spécifique.

    Attributs :
        model (Model) : Le modèle Review à créer.
        form_class (Form) : Le formulaire utilisé pour créer une Review.
        template_name (str) : Le template utilisé pour l'affichage du formulaire.
        title (str) : Titre de la page (utilisable dans le template).
        success_url (str) : URL de redirection après validation du formulaire.
    """

    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review/review_create.html'
    title = 'Ajouter une critique'
    success_url = reverse_lazy('home')

    def form_valid(self, form: ReviewForm) -> HttpResponse:
        """
        Appelé lorsque le formulaire est valide. Associe l'utilisateur
        connecté et le ticket à la critique avant de sauvegarder.

        Args:
            form (ReviewForm): Le formulaire validé.

        Returns:
            HttpResponse: La réponse HTTP redirigeant vers success_url.
        """
        form.instance.user = self.request.user
        ticket_id = self.kwargs['ticket_id']  # récupère depuis l’URL
        form.instance.ticket_id = ticket_id

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Ajoute le ticket concerné au contexte pour affichage dans le template.

        Returns:
            dict: Le contexte enrichi avec le ticket associé.
        """
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs['ticket_id']
        ticket = Ticket.objects.get(id=ticket_id)
        context['ticket'] = ticket

        return context


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vue permettant à un utilisateur authentifié de modifier une critique (Review)
    qu'il a lui-même rédigée.

    Attributs :
        model (Model) : Le modèle Review à modifier.
        form_class (Form) : Le formulaire utilisé pour la modification.
        template_name (str) : Le template utilisé pour l'affichage du formulaire.
        title (str) : Titre de la page (utilisable dans le template).
        success_url (str) : URL de redirection après validation.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review/review_update.html'
    title = 'Modifier une critique'
    success_url = reverse_lazy('home')

    def form_valid(self, form: ReviewForm) -> HttpResponse:
        """
        Appelé lorsque le formulaire est valide. Associe l'utilisateur
        connecté à la critique (par sécurité) avant de sauvegarder.

        Args:
            form (ReviewForm): Le formulaire validé.

        Returns:
            HttpResponse: La réponse HTTP de redirection.
        """
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_queryset(self):
        """
        Limite l'édition aux critiques appartenant à l'utilisateur connecté.

        Returns:
            QuerySet: Les Reviews que l'utilisateur connecté est autorisé à modifier.
        """

        return Review.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Ajoute au contexte le ticket lié à la critique en cours d'édition,
        afin qu'il soit affiché dans le template.

        Returns:
            dict: Contexte enrichi avec le ticket lié.
        """
        context = super().get_context_data(**kwargs)
        ticket = self.object.ticket
        context['ticket'] = ticket

        return context


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vue permettant à un utilisateur authentifié de supprimer une critique (Review)
    qu'il a lui-même rédigée.

    Attributs :
        model (Model) : Le modèle Review à supprimer.
        template_name (str) : Le template utilisé pour afficher la confirmation.
        success_url (str) : L'URL vers laquelle l'utilisateur est redirigé après la suppression.
    """

    model = Review
    template_name = 'reviews/review/review_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self)  -> QuerySet:
        """
        Restreint l'accès à la suppression uniquement aux critiques
        appartenant à l'utilisateur connecté.

        Returns:
            QuerySet: Les Reviews que l'utilisateur connecté peut supprimer.
        """

        return Review.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Ajoute au contexte le ticket associé à la critique,
        pour affichage dans le template de confirmation.

        Returns:
            dict: Le contexte enrichi avec le ticket lié à la critique.
        """
        context = super().get_context_data(**kwargs)
        ticket = self.object.ticket
        context['ticket'] = ticket

        return context
