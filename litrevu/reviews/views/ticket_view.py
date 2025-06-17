from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from reviews.models.ticket_model import Ticket
from reviews.forms.ticket_form import TicketForm
from django.http import HttpResponseRedirect
from django.db.models import QuerySet


class TicketCreateView(LoginRequiredMixin, CreateView):
    """
    Vue pour permettre à un utilisateur authentifié de créer un ticket.

    Affiche un formulaire vide, et à la soumission valide et enregistre un nouveau ticket
    associé à l'utilisateur connecté.

    Attributs :
        model (Model) : Le modèle lié à la vue, ici Ticket.
        form_class (Form) : Le formulaire utilisé pour la création du ticket.
        template_name (str) : Le template HTML utilisé pour afficher le formulaire.
        title (str) : Titre de la page (utilisable dans le contexte si on l'ajoute).
        success_url (str) : L’URL de redirection après la création réussie du ticket.
    """

    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket/ticket_create.html'
    title = 'Ajouter un Ticket'
    success_url = reverse_lazy('home')

    def form_valid(self, form: TicketForm) -> HttpResponseRedirect:
        """
        Associe le ticket à l'utilisateur connecté avant l'enregistrement.

        Args:
            form (TicketForm): Le formulaire validé.

        Returns:
            HttpResponseRedirect: Redirection vers la page de succès.
        """

        form.instance.user = self.request.user

        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vue pour modifier un ticket existant appartenant à l'utilisateur connecté.

    Affiche un formulaire pré-rempli avec les données du ticket sélectionné.
    À la soumission, enregistre les modifications si l'utilisateur est bien le propriétaire du ticket.

    Attributs de classe :
        model (Model) : Le modèle lié à la vue, ici Ticket.
        form_class (Form) : Le formulaire utilisé pour la mise à jour du ticket.
        template_name (str) : Le template HTML utilisé pour afficher le formulaire.
        title (str) : Titre de la page (utilisable dans le contexte si on l'ajoute).
        success_url (str) : L'URL de redirection après la mise à jour réussie du ticket.
    """

    model = Ticket
    form_class = TicketForm
    template_name = 'reviews/ticket/ticket_update.html'
    title = 'Modifier un Ticket'
    success_url = reverse_lazy('home')

    def form_valid(self, form: TicketForm) -> HttpResponseRedirect:
        """
        Associe l'utilisateur connecté au ticket modifié.

        Args:
            form (TicketForm): Le formulaire validé.

        Returns:
            HttpResponseRedirect: Redirection vers la page de succès.
        """
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_queryset(self) -> QuerySet:
        """
        Limite l'accès aux tickets appartenant à l'utilisateur connecté.

        Returns:
            QuerySet: Tickets filtrés.
        """

        return Ticket.objects.filter(user=self.request.user)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vue pour supprimer un ticket appartenant à l'utilisateur connecté.

    Affiche une page de confirmation de suppression.
    Si l'utilisateur confirme et est bien le propriétaire du ticket, celui-ci est supprimé.

    Attributs de classe :
        model (Model) : Le modèle lié à la vue, ici Ticket.
        template_name (str) : Le template HTML utilisé pour la page de confirmation.
        success_url (str) : L'URL de redirection après suppression du ticket.
    """

    model = Ticket
    template_name = 'reviews/ticket/ticket_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        """
        Limite l'accès à la suppression aux tickets de l'utilisateur connecté.

        Returns:
            QuerySet: Tickets filtrés.
        """

        return Ticket.objects.filter(user=self.request.user)
