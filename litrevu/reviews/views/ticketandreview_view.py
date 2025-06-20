from django.views import View
from django.shortcuts import render, redirect
from reviews.forms import TicketForm, ReviewForm
from reviews.models import Ticket, Review
from itertools import chain
from operator import attrgetter
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class ReviewAndTicketCreateView(LoginRequiredMixin, View):
    """
    Vue pour créer simultanément un ticket et une critique associée.

    Cette vue permet à un utilisateur authentifié de remplir deux formulaires
    (un pour le ticket, un pour la critique) sur une seule page, et de les enregistrer
    si les deux sont valides.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Affiche un formulaire vide pour créer un ticket et une critique en même temps.

        :param request: Requête HTTP GET envoyée par l'utilisateur.
        :return: Page HTML avec les deux formulaires vides.
        """

        ticket_form = TicketForm()
        review_form = ReviewForm()

        return render(request, 'reviews/ticketandreview_create.html', {
            'ticket_form': ticket_form,
            'review_form': review_form
        })

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Traite l'envoi des deux formulaires (ticket et critique).

        Si les deux formulaires sont valides :
        - Crée le ticket en l'associant à l'utilisateur connecté.
        - Crée la critique en l'associant à l'utilisateur connecté et au ticket.

        :param request: Requête HTTP POST contenant les données des deux formulaires.
        :return: Redirection vers la page d'accueil si succès, sinon réaffiche les formulaires avec erreurs.
        """

        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            # On utilise commit=False pour ne pas enregistrer tout de suite
            # Cela permet d’ajouter manuellement des champs
            # comme user ou ticket (FK) avant de faire le save()

            return redirect('home')

        return render(request, 'reviews/ticketandreview_create.html', {
            'ticket_form': ticket_form,
            'review_form': review_form
        })


class PostsView(LoginRequiredMixin, View):
    """
    Vue pour afficher tous les posts (tickets et critiques) créés par l'utilisateur connecté.

    Cette vue combine les tickets et les critiques de l'utilisateur, puis les trie par date
    de création de manière antéchronologique (du plus récent au plus ancien).
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Récupère tous les tickets et critiques créés par l'utilisateur,
        les fusionne et les trie par date de création (décroissante).

        :param request: Requête HTTP GET envoyée par l'utilisateur.
        :return: Page HTML affichant la liste des posts (tickets + critiques) de l'utilisateur.
        """

        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)

        # Combiner les deux QuerySets
        combined = list(chain(tickets, reviews))

        # Trier par timestamp dans l'ordre antéchronologique
        combined.sort(key=attrgetter('time_created'), reverse=True)

        context = {
            'posts': combined,
        }

        return render(request, 'reviews/posts.html', context)
