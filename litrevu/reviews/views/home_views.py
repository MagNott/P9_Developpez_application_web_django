from django.shortcuts import render
from reviews.models import Ticket, Review, UserFollows
from authentication.models import User
from django.views import View
from itertools import chain
from operator import attrgetter
from django.contrib.auth.mixins import LoginRequiredMixin


class FeedView(LoginRequiredMixin, View):
    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)

        # Version raccroucie d'une compréhension de liste
        followed_users = [f.followed_user for f in UserFollows.objects.filter(user=request.user)]

        tickets_followed = Ticket.objects.filter(user__in=followed_users)
        reviews_followed = Review.objects.filter(user__in=followed_users)

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

        context = {
            'feeds': combined,
        }

        return render(request, 'reviews/home.html', context)
