from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from .ticket_model import Ticket


class Review(models.Model):
    """
    Modèle représentant une critique (review) d'un ticket.

    Chaque critique est liée à un ticket et à un utilisateur.
    Elle contient une note, un titre (headline), un corps de texte (body)
    et une date de création automatique.
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
