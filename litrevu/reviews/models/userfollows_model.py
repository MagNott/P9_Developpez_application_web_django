from django.conf import settings
from django.db import models


class UserFollows(models.Model):
    """
    Modèle représentant une relation de suivi entre deux utilisateurs.

    - `user` : l'utilisateur qui suit quelqu'un.
    - `followed_user` : l'utilisateur qui est suivi.

    Exemple : si A suit B, alors :
        user = A
        followed_user = B
    """

    # L'utilisateur qui suit un autre utilisateur
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following"
    )

    # L'utilisateur qui est suivi
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    class Meta:
        # Empêche de créer deux fois la même relation de suivi entre deux
        # utilisateurs
        unique_together = (
            "user",
            "followed_user",
        )
