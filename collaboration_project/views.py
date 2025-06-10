from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from myapp.models import project_comment, project_reply, projects, userinfo, Notification
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from myapp.utils import send_notification_email


@login_required
def toggle_like_project_comment(request, comment_id):
    comment_obj = get_object_or_404(project_comment, id = comment_id)
    userinfo_obj = request.user.info
    comment_owner = comment_obj.user
    if userinfo_obj in comment_obj.likes.all():
        comment_obj.likes.remove(userinfo_obj)
        liked = False
        if userinfo_obj != comment_owner:
            Notify_obj = Notification.objects.filter(user=comment_owner, sender=userinfo_obj, notification_type="project_comment_like", project_comment=comment_obj)
            if Notify_obj:
                Notify_obj.delete()
       
    else:
        comment_obj.likes.add(userinfo_obj)
        liked = True
        if userinfo_obj != comment_owner:
            Notification.objects.create(user=comment_owner, sender=userinfo_obj, notification_type="project_comment_like", project_comment=comment_obj)
       
    return JsonResponse({'liked': liked, 'total_likes': comment_obj.total_likes()}) 


@login_required
def toggle_like_reply(request, reply_id):
    reply_obj = get_object_or_404(project_reply, id = reply_id)
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
def save_project_reply(request):
    content = request.POST.get('reply_content', '').strip()
    comment_id = request.POST.get('comment_id')
    userinfo_obj = get_object_or_404(userinfo, user=request.user)

    if not content:
        return JsonResponse({'success': False, 'error': 'Reply content cannot be empty.'})

    try:
        comment = project_comment.objects.get(id=comment_id)
    except project_comment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Parent comment not found.'})

    reply = project_reply.objects.create(
        user=request.user.info,
        comment=comment,
        content=content
    )

    rendered_reply = render_to_string('collaboration_project/reply_card.html', {
        'reply': reply,
        'user': request.user,
    }, request=request)
    
    if comment.user != userinfo_obj:
        notify = Notification.objects.create(user=reply.comment.user, sender=userinfo_obj, project_reply=reply, notification_type='project_reply')
        send_notification_email(reply.comment.user, f'🧑‍💻 {userinfo_obj.user.username} {notify.get_notification_type_display()} on \"{reply.comment.project.title}\"!\n\n💬 {reply.content[:50]}...')

    return JsonResponse({'success': True, 'reply_html': rendered_reply, 'total_comments': comment.project.tot_comments(), 'show_replies_count': comment.replies.count()})

@require_POST
@login_required
def save_project_comment(request, project_id):
    content = request.POST.get('content')
    userinfo_obj = get_object_or_404(userinfo, user=request.user)
    if not content.strip():
        return JsonResponse({'success': False, 'error': 'Comment cannot be empty.'})

    try:
        project = projects.objects.get(id=project_id)
        comment = project_comment.objects.create(
            user=request.user.info,
            content=content,
            project=project
        )

        comment_html = render_to_string('collaboration_project/comment_card.html', {
            'comment': comment,
            'user': request.user
        }, request=request)

        total_comments = project.tot_comments()
        
        if project.creator != userinfo_obj:
            notify = Notification.objects.create(user= project.creator, sender=userinfo_obj, project_comment=comment, notification_type = 'project_comment')
            send_notification_email(project.creator, f"🧑‍💻 {userinfo_obj.user.username} just {notify.get_notification_type_display()} \"{comment.project.title}\"!\n\n💬 {comment.content[:50]}...")
        
        return JsonResponse({'success': True, 'comment_html': comment_html, 'total': total_comments})
    
    except projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found.'})
    

