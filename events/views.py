from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from myapp.models import event_comment, event_reply, event, userinfo, Notification
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from myapp.utils import send_notification_email

@login_required
def toggle_like_comment(request, comment_id):
    comment_obj = get_object_or_404(event_comment, id = comment_id)
    userinfo_obj = request.user.info
    comment_owner = comment_obj.user
    if userinfo_obj in comment_obj.likes.all():
        comment_obj.likes.remove(userinfo_obj)
        liked = False
        if userinfo_obj != comment_owner and comment_owner:
            Notify_obj = Notification.objects.filter(user=comment_owner, sender=userinfo_obj, notification_type="event_comment_like", event_comment=comment_obj)
            if Notify_obj:
                Notify_obj.delete()
    else:
        comment_obj.likes.add(userinfo_obj)
        liked = True
        if userinfo_obj != comment_owner and comment_owner:
            Notification.objects.create(user=comment_owner, sender=userinfo_obj, notification_type="event_comment_like", event_comment=comment_obj)
            
    return JsonResponse({'liked': liked, 'total_likes': comment_obj.total_likes()}) 

@login_required
def toggle_like_reply(request, reply_id):
    reply_obj = get_object_or_404(event_reply, id = reply_id)
    userinfo_obj = request.user.info
    if userinfo_obj in reply_obj.likes.all():
        reply_obj.likes.remove(userinfo_obj)
        liked = False
    else:
        reply_obj.likes.add(userinfo_obj)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': reply_obj.total_likes()}) 


@require_POST
@login_required
def save_event_comment(request, event_id):
    content = request.POST.get('content')
    userinfo_obj = get_object_or_404(userinfo, user=request.user)
    
    if not content.strip():
        return JsonResponse({'success': False, 'error': 'Comment cannot be empty.'})

    try:
        event_obj = event.objects.get(id=event_id)
        comment = event_comment.objects.create(
            user=request.user.info,
            content=content,
            event=event_obj
        )

        comment_html = render_to_string('events/comment_card.html', {
            'comment': comment,
            'user': request.user
        }, request=request)

        total_comments = event_obj.tot_comments()
        
        if event_obj.organization.user != request.user:
            notify = Notification.objects.create(user=comment.event.organization.user.info, sender=userinfo_obj, event_comment=comment, notification_type='event_comment')
            send_notification_email(comment.event.organization.user.info, f'🧑‍💻 {userinfo_obj.user.username} {notify.get_notification_type_display()} \"{comment.event.title}\"!\n\n💬 {comment.content[:50]}...')
        
        return JsonResponse({'success': True, 'comment_html': comment_html, 'total': total_comments})
    
    except event.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found.'})
    

@login_required
@require_POST
def save_event_reply(request):
    content = request.POST.get('reply_content', '').strip()
    comment_id = request.POST.get('comment_id')
    userinfo_obj = get_object_or_404(userinfo, user=request.user)

    if not content:
        return JsonResponse({'success': False, 'error': 'Reply content cannot be empty.'})

    try:
        comment = event_comment.objects.get(id=comment_id)
    except event_comment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Parent comment not found.'})

    reply = event_reply.objects.create(
        user=request.user.info,
        comment=comment,
        content=content
    )

    rendered_reply = render_to_string('events/reply_card.html', {
        'reply': reply,
        'user': request.user,
    }, request=request)
    
    if comment.user != userinfo_obj:
        notify = Notification.objects.create(user=reply.comment.user, sender=userinfo_obj, event_reply=reply, notification_type='event_reply')
        send_notification_email(reply.comment.user, f'🧑‍💻 {userinfo_obj.user.username} {notify.get_notification_type_display()} on Event \"{reply.comment.event.title}\"!\n\n💬 {reply.content[:50]}...')

    return JsonResponse({'success': True, 'reply_html': rendered_reply, 'total_comments': comment.event.tot_comments(), 'show_replies_count': comment.replies.count()})

