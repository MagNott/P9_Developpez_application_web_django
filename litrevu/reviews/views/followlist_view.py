from django.views import View
from django.shortcuts import render
from reviews.models import UserFollows
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


class FollowListView(View):

    def get(self, request):
        followers = UserFollows.objects.filter(followed_user=request.user)
        following = UserFollows.objects.filter(user=request.user)
        search_query = request.GET.get("search", "")
        User = get_user_model()
        followed_users = [f.followed_user for f in UserFollows.objects.filter(user=request.user)]

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

    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get("user_id")
        User = get_user_model()
        followed_user = User.objects.get(id=followed_user_id)

        UserFollows.objects.create(user=request.user, followed_user=followed_user)

        return redirect("follow")


class UnfollowView(View):

    def get(self, request, followed_user_id):
        User = get_user_model()
        user_to_unfollow = User.objects.get(id=followed_user_id)

        context = {
            "user_to_unfollow": user_to_unfollow
        }

        return render(request, 'reviews/unfollow.html', context)



    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get("user_id")

        follow_delete = UserFollows.objects.filter(user=request.user, followed_user__id=followed_user_id)

        if (follow_delete).exists():
            follow_delete.delete()
            return redirect ("follow")