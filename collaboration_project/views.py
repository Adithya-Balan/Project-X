from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from myapp.models import project_comment, project_reply, projects, userinfo, Notification, SavedItem
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from myapp.utils import send_notification_email
from myapp.forms import PostForm
from .forms import ProjectForm
from django.core.paginator import Paginator, PageNotAnInteger

@login_required
def project_detail(request, id):
    project = projects.objects.get(id = id)
    userinfo_obj = project.creator
    link_available = False
    all_comment = request.GET.get('all_comment')
    social_links = { 
        'github': userinfo_obj.github if userinfo_obj.github else None,
        'linkedin': userinfo_obj.linkedin if userinfo_obj.linkedin else None,
        'stack-overflow': userinfo_obj.stackoverflow if userinfo_obj.stackoverflow else None,
    }
    if social_links.get('github') or social_links.get('linkedin') or social_links.get('stackoverflow'):
            link_available = True
            
    comments = project.forum.all()
    if not all_comment:
        comments = comments.order_by('-created_at')
        
    post_form = PostForm()
    context = {
        'project': project,
        'skill_needed': project.skill_needed.all(),
        'link_available': link_available,
        'social_link': social_links,
        'comments': comments,
        'post_form': post_form,
    }
    return render(request, 'collaboration_project/project_detail.html', context)


@login_required
def project_joined_members(request, id):
    project = get_object_or_404(projects, id = id)
    members =  project.members.all()
    post_form = PostForm()
    
    p = Paginator(members, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = p.page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    context = {
        'project_obj': project,
        'post_form': post_form,
        'joined_members': page_obj,
    }
    return render(request, 'collaboration_project/project-member-list.html', context)

@login_required
def join_project(request, id):
    project = get_object_or_404(projects, id=id)
    userinfo_obj = get_object_or_404(userinfo, user=request.user)
    if userinfo_obj in project.members.all():
        project.members.remove(userinfo_obj)
        joined = False
        Notification.objects.filter(user=project.creator, sender=userinfo_obj, project=project, notification_type='Join_Project').delete()
    else:
        project.members.add(userinfo_obj)
        joined = True
        if userinfo_obj != project.creator:
            notify = Notification.objects.create(user=project.creator, sender=userinfo_obj, project=project, notification_type='Join_Project')
            send_notification_email(project.creator, f'🧑‍💻 {userinfo_obj.user.username} {notify.get_notification_type_display()} \"{notify.project.title}\" 🚀')
    return JsonResponse({"joined": joined, "total_member": project.tot_member()})

@login_required
def project_form(request):
    post_form = PostForm()
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            print(True)
            project = form.save(commit=False)
            project.creator = request.user.info
            project.save()
            form.save_m2m()
            return redirect(f"{reverse('project_detail', args=[project.id])}")
            
    context = {
        'post_form': post_form,
        'form': form,
        'is_edit': False,
    }
    return render(request, 'collaboration_project/project-form.html', context)

@login_required
def project_form_edit(request, uuid):
    post_form = PostForm()
    project_obj = get_object_or_404(projects, uuid = uuid)
    if project_obj.creator == request.user.info:
        form = ProjectForm(instance=project_obj)
        if request.method == "POST":
            form = ProjectForm(request.POST, request.FILES, instance=project_obj)
            if form.is_valid():
                project = form.save()
                return redirect(f"{reverse('project_detail', args=[project.id])}")
        context = {
            'post_form': post_form,
            'form': form,
            'is_edit': True,
            'project_obj': project_obj,
        }
        return render(request, 'collaboration_project/project-form.html', context)
    else:
        return redirect("/")
    
@login_required
def toggle_project_save(request, project_id):
    project_obj = get_object_or_404(projects, id=project_id)
    saved_items_obj = SavedItem.objects.get(user=request.user.info)
    
    if project_obj in saved_items_obj.project.all():
        saved_items_obj.project.remove(project_obj)
        saved = False
    else:
        saved_items_obj.project.add(project_obj)
        saved = True
        
    return JsonResponse({
        'saved': saved,
    })

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
    
@login_required
def delete_project(request, uuid):
    project_obj = get_object_or_404(projects, uuid = uuid)
    reverse_url = f"{reverse('user_profile', args=[request.user.username])}?section=projects"
    if project_obj.creator == request.user.info:
        project_obj.delete()
        return redirect(reverse_url) 
    return redirect('/')
    

