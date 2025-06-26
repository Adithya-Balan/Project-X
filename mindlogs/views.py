from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import MindLogForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import MindLog
from .utils import get_24h_mindlog_stats
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from collections import Counter
from datetime import timedelta
from django.db.models import Avg
from django.contrib import messages

@login_required
def explore_logs_page(request):
    mindlog_obj = get_24h_mindlog_stats()
    logs_qs = mindlog_obj['logs_qs']
    
    paginator = Paginator(logs_qs, 20)  # 20 logs per page
    page_obj = paginator.page(1)
   
    context = {
        "mindlog_obj": mindlog_obj,
        "logs_qs": page_obj.object_list,
        "has_next": page_obj.has_next(),
    }
    return render(request, "mindlogs/logs.html", context)

#load more option for explore logs
@login_required
def load_more_logs(request):
    page = int(request.GET.get("page", 1))
    logs_qs = MindLog.objects.filter(timestamp__gte=timezone.now() - timedelta(hours=24)).order_by("-timestamp")
    paginator = Paginator(logs_qs, 20)

    try:
        logs_page = paginator.page(page)
    except:
        return JsonResponse({"logs_html": "", "has_next": False})

    html = render_to_string("partials/log_cards.html", {"logs_qs": logs_page.object_list, "user": request.user}, request=request )
    return JsonResponse({
        "logs_html": html,
        "has_next": logs_page.has_next()
    })

@login_required
def terminal_page(request):
    logform = MindLogForm()
    context = {
        'logform': logform,
    }
    return render(request, "mindlogs/log_terminal.html", context)

# for personal log book
@login_required
def personal_logbook(request, username):
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return render(request, 'mindlogs/logs_user_not_found.html', {"username": username})
        
    info = user.info
    logs = MindLog.objects.filter(user = info).order_by("-timestamp")
    total_logs = logs.count()
    last_log_date = timezone.localtime(logs.first().timestamp).date() if total_logs else None
    # Avg Latency
    avg_latency = int(logs.aggregate(avg=Avg('latency'))['avg']) if total_logs else 0

    # Top Used Neurocolor
    colors = list(logs.exclude(neuro_color__isnull=True).values_list('neuro_color', flat=True))
    top_color = Counter(colors).most_common(1)[0][0] if colors else None
    
    # Streak calculation
    today = timezone.now().date()
    streak = 0
    seen_days = set(log.timestamp.date() for log in logs)

    for i in range(0, 365):
        day = today - timedelta(days=i)
        if day in seen_days:
            streak += 1
        else:
            break

    # Clone Impact
    clone_impact = MindLog.objects.filter(original_log__user=info).count()
    
    paginator = Paginator(logs, 20)  # 20 logs per page
    page_obj = paginator.page(1)

    context = {
        "mindlogs": page_obj.object_list,
        'userinfo_obj': info,
        "total_logs": total_logs,
        "last_log_date": last_log_date.strftime("%b %d, %Y") if last_log_date else "—",
        "avg_latency": avg_latency,
        "top_color": top_color,
        "streak": streak,
        "clone_impact": clone_impact,
        "has_next": page_obj.has_next(),
    }
    return render(request, "mindlogs/personal_logbook.html", context)

#load more option for explore logs
@login_required
def load_more_personal_logs(request, username):
    user = get_object_or_404(User, username = username)
    info = user.info
    page = int(request.GET.get("page", 1))
    logs = MindLog.objects.filter(user = info).order_by("-timestamp")
    paginator = Paginator(logs, 20)

    try:
        logs_page = paginator.page(page)
    except:
        return JsonResponse({"logs_html": "", "has_next": False})

    html = render_to_string("partials/personal_log_cards.html", {"mindlogs": logs_page.object_list, "user": request.user}, request=request)
    return JsonResponse({
        "logs_html": html,
        "has_next": logs_page.has_next()
    })

@require_POST
@login_required
def save_mindlog(request):
    if request.method == "POST":
        logform = MindLogForm(request.POST or None)
        if logform.is_valid():
            log = logform.save(commit=False)
            log.user = request.user.info
            log.save()
            
            messages.success(request, "Log committed successfully!")
            return redirect("explore_logs_page")
    return redirect(request.META.get('HTTP_REFERER', '/'))
    

#save clone log
@login_required
def save_clone_log(request, sig):
    user = request.user.info
    original_log = get_object_or_404(MindLog, sig=sig)
    
    if original_log.user == user:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if original_log.original_log and original_log.original_log.user == user:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    root_log = original_log.original_log if original_log.original_log else original_log
    clone = MindLog.objects.create(
        user=user,
        content=original_log.content,
        neuro_color=original_log.neuro_color,
        latency=original_log.latency,
        original_log=root_log
    )
    root_log.clone_count = root_log.clones.count()
    root_log.save()
    messages.success(request, "Log cloned successfully!")
    return redirect(f"{reverse('personal_logbook', args=[request.user.username])}")


@login_required
@require_POST
def delete_log(request, sig):
    userinfo = request.user.info
    try:
        log = MindLog.objects.get(sig=sig)
    except MindLog.DoesNotExist:
        return JsonResponse({'error': 'Log not found'}, status=404)

    if log.user != userinfo:
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

    log.delete()
    return JsonResponse({'success': True})


def mindbook(request):
    return render(request, "mindlogs/mindbook.html")