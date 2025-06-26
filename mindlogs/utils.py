from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from .models import MindLog
import math


def get_24h_mindlog_stats():
    now = timezone.now()
    last_24h = now - timedelta(hours=24)

    logs_qs = MindLog.objects.filter(timestamp__gte=last_24h).order_by("-timestamp")
    
    stats = {
        "logs_qs": logs_qs,
        "logs_fired": logs_qs.count(),
        "logs_per_min": math.ceil(logs_qs.count() / (24 * 60)),
        "mean_latency": round(logs_qs.aggregate(Avg('latency'))['latency__avg'] or 0),
        "clones_today": logs_qs.filter(original_log__isnull=False).count(),
    }
    return stats


