from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from myapp.models import event_comment, event_reply, event, userinfo, Notification, organization, SavedItem
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from myapp.utils import send_notification_email
from myapp.forms import PostForm
from .forms import EventForm

def event_detail(request, id):
    event_obj = get_object_or_404(event, pk=id)
    post_form = PostForm()
    comments = event_obj.forum.all().order_by('-created_at') 
    context = {
        'event_obj': event_obj,
        'post_form' : post_form,
        'comments': comments,
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def org_event_form(request,id):
    organization_obj = get_object_or_404(organization, id = id)
    createdByUser = True if organization_obj.user == request.user else False
    post_form = PostForm()
    if createdByUser:
        form = EventForm()
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                event_obj = form.save(commit=False)
                event_obj.organization = organization_obj
                event_obj.save()
                return redirect('event_detail', event_obj.id)
    else:
        return redirect('/')
    context = {
        'event_form': form,
        'is_edit': False,
        'post_form': post_form,
    }
    return render(request, 'events/org-event-form.html', context)

@login_required
def event_form_edit(request, org_id, event_id):
    organization_obj = get_object_or_404(organization, id = org_id)
    event_obj = get_object_or_404(event, id = event_id)
    createdByUser = True if organization_obj.user == request.user else False
    post_form = PostForm()
    if createdByUser:
        form = EventForm(instance=event_obj)
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES, instance=event_obj)
            print(form)
            if form.is_valid():
                form.save()
                return redirect('event_detail', event_obj.id)
    else:
        return redirect('/')
    context = {
        'event_form': form,
        'is_edit': True,
        'post_form': post_form,
        'event_obj': event_obj,
    }
    return render(request, 'events/org-event-form.html', context)

@login_required
# Toggle saving events
def toggle_event_save(request, eventId):
    event_obj = get_object_or_404(event, id = eventId)
    saved_items_obj = SavedItem.objects.get(user=request.user.info)
    if event_obj in saved_items_obj.events.all():
        saved_items_obj.events.remove(event_obj)
        saved = False
    else:
        saved_items_obj.events.add(event_obj)
        saved = True
    return JsonResponse({
        'saved': saved,
    })
    
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
        return JsonResponse({'success': False, 'error': 'Event not found.'})
    

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

@login_required
def delete_event(request,uuid):
    event_obj = get_object_or_404(event, uuid = uuid)
    reverse_url = f"{reverse('organization_detail', args=[event_obj.organization.id])}?section=events"
    if event_obj.organization.user == request.user:
        event_obj.delete()
        return redirect(reverse_url) 
    return redirect('/')