from django.shortcuts import render
from reviews.models import Ticket, Review, UserFollows
from django.views import View
from itertools import chain
from operator import attrgetter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse


class FeedView(LoginRequiredMixin, View):
    """
    Vue permettant d'afficher le flux personnalisé de l'utilisateur connecté.

    Le flux contient :
    - Les tickets et critiques créés par l'utilisateur
    - Les tickets et critiques créés par les utilisateurs qu'il suit

    Tous les objets sont annotés d'un attribut 'content_type' (TICKET ou REVIEW)
    pour pouvoir les distinguer dans le template.

    Les éléments sont triés par date de création décroissante.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Gère la requête GET pour afficher le flux d'activité.

        Args:
            request (HttpRequest): La requête HTTP contenant les informations de l'utilisateur connecté.

        Returns:
            HttpResponse: La page HTML affichant les éléments du flux (tickets et critiques).
        """
        # Récupérer les tickets et review de l'utilisateur connecté
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)

        # Récupérer tous les utilisateurs suivis de l'utilisateur connecté
        followed_users = [f.followed_user for f in UserFollows.objects.filter(user=request.user)]

        # Récupérer les tickets des utilisateurs suivis par l'utilisateur connecté
        tickets_followed = Ticket.objects.filter(user__in=followed_users)

        # Récupérer les critiques écrites par des utilisateurs suivis
        # uniquement si les tickets liés ont aussi été créés par des utilisateurs suivis
        reviews_followed = Review.objects.filter(user__in=followed_users, ticket__user__in=followed_users)

        # Ajout d'un attribut pour discriminer le type d'objet dans la vue
        for ticket in tickets:
            ticket.content_type = "TICKET"

        for review in reviews:
            review.content_type = "REVIEW"

        for ticket in tickets_followed:
            ticket.content_type = "TICKET"

        for review in reviews_followed:
            review.content_type = "REVIEW"

        # Combiner les deux QuerySets
        combined = list(chain(tickets, reviews, tickets_followed, reviews_followed))

        # Trier par timestamp dans l'ordre antéchronologique
        combined.sort(key=attrgetter('time_created'), reverse=True)

        # On récupère toutes les reviews de l'utilisateur connecté
        # Cela permettra, dans le template, de vérifier si une critique existe
        # déjà pour un ticket affiché et d’afficher soit le bouton "Créer une
        # critique", soit "Modifier la critique" en conséquence
        user_reviews = Review.objects.filter(user=request.user)

        user_reviewed_ticket_ids = [review.ticket.id for review in user_reviews]

        context = {
            'feeds': combined,
            "user_reviews": user_reviews,
            'user_reviewed_ticket_ids': user_reviewed_ticket_ids,
        }

        return render(request, 'reviews/home.html', context)
