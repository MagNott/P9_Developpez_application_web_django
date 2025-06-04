from django.views import View
from django.shortcuts import render
from reviews.models import Ticket, Review
from itertools import chain
from operator import attrgetter


class PostsView(View):
    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)

        # Combiner les deux QuerySets
        combined = list(chain(tickets, reviews))

        # Triez-les par timestamp dans l'ordre antéchronologique
        combined.sort(key=attrgetter('time_created'), reverse=True)

        context = {
            'posts': combined,
        }

        return render(request, 'reviews/posts.html', context)
