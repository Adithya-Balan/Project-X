from .models import userinfo, follow

def get_explore_users(filter_dev, request, count=200):
    # Step 1: Get followed user IDs and current user ID
    followed_ids = follow.objects.filter(
        follower=request.user.info
    ).values_list('following_id', flat=True)

    exclude_ids = list(followed_ids) + [request.user.info.id]

    # Step 2: Use `.only()` to limit fields fetched from DB for performance
    users = filter_dev.exclude(id__in=exclude_ids).only('id', 'profile_image', 'user__username').order_by('?')[:count]
    return users
