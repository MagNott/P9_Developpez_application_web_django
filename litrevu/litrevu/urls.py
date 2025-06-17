"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

import reviews.models.review_model
from reviews.views.home_views import FeedView

# Imports pour l'authetification
from django.contrib.auth.views import LoginView
from authentication.views import SignupView

# Imports pour les tickets
from reviews.views.ticket_view import TicketCreateView
from reviews.views.ticket_view import TicketUpdateView
from reviews.views.ticket_view import TicketDeleteView

# Imports pour les critiques
from reviews.views.review_view import ReviewCreateView
from reviews.views.review_view import ReviewUpdateView
from reviews.views.review_view import ReviewDeleteView

# Import pour la vue combinée créer ticket et critique en même temps
from reviews.views.ticketandreview_view import ReviewAndTicketCreateView
from reviews.views.ticketandreview_view import PostsView

from reviews.views.followlist_view import FollowListView
from reviews.views.followlist_view import UnfollowView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Routes pour l'authetification
    path('login/', LoginView.as_view(template_name='authentication/login.html', redirect_authenticated_user=True), name='login'),
    path('signup/', SignupView.as_view(template_name='authentication/signup.html'), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('home/', FeedView.as_view(), name='home'),

    # Routes liées aux tickets
    path('ticket/create/', TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/update/<int:pk>/', TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/delete/<int:pk>/', TicketDeleteView.as_view(), name='ticket-delete'),

    # Routes pour reviews
    path('review/create/<int:ticket_id>/', ReviewCreateView.as_view(), name='review-create'),
    path('review/update/<int:pk>/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/delete/<int:pk>/', ReviewDeleteView.as_view(), name='review-delete'),

    # Routes combinée pour créer un ticket et une review en même temps
    path('ticketandreview/create/', ReviewAndTicketCreateView.as_view(), name='ticketandreview_create'),

    # Posts qui affiche les tickets et les revues de la personne connectée
    path('posts/', PostsView.as_view(), name='posts'),

    # Abonnements qui affiche les abonnés et les abonnements
    path('follow/', FollowListView.as_view(), name='follow'),
    path('unfollow/<int:followed_user_id>/', UnfollowView.as_view(), name='unfollow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)