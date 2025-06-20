from django.db import models
from django.conf import settings
from PIL import Image


class Ticket(models.Model):
    """
    Modèle représentant un ticket (demande de critique).

    Un ticket est créé par un utilisateur, et peut contenir :
    - un titre
    - une description optionnelle
    - une image optionnelle
    - une date de création automatique
    """

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour redimensionner l'image avant sauvegarde,
        si une image est présente. La taille maximale est de 800x800 pixels.
        """
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((800, 800))  # taille max
            img.save(self.image.path)
