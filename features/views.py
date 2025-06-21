from django.shortcuts import render
from .models import TrendingLeaderboard

# Create your views here.
def leaderboard_page(request):
    leaderboard = TrendingLeaderboard.objects.all()[:11]
    top_3 = leaderboard[:3]
    remaining_7 = leaderboard[3:11] 
    remaining_7 = TrendingLeaderboard.objects.all()[3:25]
    context = {
        'top_1': top_3[0] if len(top_3) > 0 else None,
        'top_2': top_3[1] if len(top_3) > 1 else None,
        'top_3': top_3[2] if len(top_3) > 2 else None,
        'remaining_7': remaining_7,
    }
    return render(request, 'features/leaderboard.html', context)

def feed_page(request):
    return render(request, 'features/feed.html',context)
