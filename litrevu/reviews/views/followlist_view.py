from django.views import View
from django.shortcuts import render
from reviews.models import UserFollows
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse


class FollowListView(View):
    """
    Vue permettant d'afficher la liste des abonnements et abonnés,
    de rechercher des utilisateurs, et d'ajouter un nouvel abonnement.

    GET : Affiche la liste des abonnements, des abonnés et les résultats de recherche.
    POST : Crée une relation de suivi entre l'utilisateur connecté et un autre utilisateur.
    """

    def get(self, request) -> HttpResponse:
        """
        Récupère et affiche :
        - les utilisateurs suivis par l'utilisateur connecté,
        - les utilisateurs qui suivent l'utilisateur connecté,
        - les résultats de recherche si une requête est soumise.

        Args:
            request (HttpRequest) : La requête HTTP entrante.

        Returns:
            HttpResponse : La page HTML affichant les informations.
        """

        # Récupérer les abonnements et les abonnés de l'utilisateur connecté
        followers = UserFollows.objects.filter(followed_user=request.user)
        following = UserFollows.objects.filter(user=request.user)

        # Récupérer ce qui est écrit dans le champs de recherche du formulaire
        search_query = request.GET.get("search", "")

        # Récupère le model utilisateur personnalisé
        User = get_user_model()

        # Récupérer les utilisateurs suivis par l'utilisateur connecté
        followed_users = [f.followed_user for f in UserFollows.objects.filter(user=request.user)]

        # Recherche des utilisateurs dont le nom d'utilisateur contient la saisie,
        # en excluant l'utilisateur actuellement connecté
        search_results = []
        if search_query:
            search_results = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)

        context = {
            'followers': followers,
            'following': following,
            "search_results": search_results,
            'followed_users': followed_users
        }

        return render(request, 'reviews/follow.html', context)

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """
        Crée un nouvel abonnement pour l'utilisateur connecté.

        Args:
            request (HttpRequest) : La requête HTTP contenant l'ID de l'utilisateur à suivre.

        Returns:
            HttpResponseRedirect : Redirige vers la page de suivi.
        """

        # Récupère l'identifiant de l'utilisateur à suivre depuis le formulaire envoyé en POST
        followed_user_id = request.POST.get("user_id")

        # Récupère le modèle utilisateur personnalisé
        User = get_user_model()

        # Recherche dans la base de données l'utilisateur correspondant à l'identifiant récupéré
        followed_user = User.objects.get(id=followed_user_id)

        # Crée une nouvelle relation de suivi entre l'utilisateur connecté et l'utilisateur ciblé
        UserFollows.objects.create(user=request.user, followed_user=followed_user)

        return redirect("follow")


class UnfollowView(View):
    """
    Vue permettant d'afficher une confirmation de désabonnement
    et de supprimer un abonnement existant.

    GET : Affiche la page de confirmation de désabonnement.
    POST : Supprime la relation de suivi si elle existe.
    """

    def get(self, request, followed_user_id: int) -> HttpResponse:
        """
        Affiche une page demandant la confirmation pour se désabonner d'un utilisateur.

        Args:
            request (HttpRequest) : La requête HTTP.
            followed_user_id (int) : L'ID de l'utilisateur à ne plus suivre.

        Returns:
            HttpResponse : La page HTML de confirmation.
        """

        # Récupère le modèle utilisateur personnalisé
        User = get_user_model()

        # Récupère l'utilisateur à ne plus suivre grâce à son identifiant
        user_to_unfollow = User.objects.get(id=followed_user_id)

        context = {
            "user_to_unfollow": user_to_unfollow
        }

        return render(request, 'reviews/unfollow.html', context)

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """
        Supprime une relation de suivi entre l'utilisateur connecté et un autre utilisateur.

        Args:
            request (HttpRequest) : La requête HTTP contenant l'ID de l'utilisateur à désabonner.

        Returns:
            HttpResponseRedirect : Redirige vers la page de suivi.
        """

        # Récupère l'id de l'utilisateur à ne plus suivre
        followed_user_id = request.POST.get("user_id")

        # prépare la requête pour pour retrouver la relation de suivi entre l'utilisateur connecté et l'utilisateur ciblé
        follow_delete = UserFollows.objects.filter(user=request.user, followed_user__id=followed_user_id)

        # Si la relation de suivi existe, on la supprime
        if (follow_delete).exists():
            follow_delete.delete()

            return redirect("follow")
