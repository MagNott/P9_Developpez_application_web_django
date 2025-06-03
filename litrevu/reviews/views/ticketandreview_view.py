from django.views import View
from django.shortcuts import render, redirect
from reviews.forms import TicketForm, ReviewForm


class ReviewAndTicketCreateView(View):
    def get(self, request):
        ticket_form = TicketForm()
        review_form = ReviewForm()
        return render(request, 'reviews/ticketandreview_create.html', {
            'ticket_form': ticket_form,
            'review_form': review_form
        })

    def post(self, request):
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
