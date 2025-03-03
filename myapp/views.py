import base64
import uuid
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.views import View
from .forms import RegistrationForm, EditProfileForm,OrganizationForm, EditEducationForm, EditExperienceForm, PostForm, UserProjectForm, EditSkillForm, EditCurrentPositionForm
from django.contrib.auth.models import User
from .models import userinfo, projects, Domain, skill, project_comment, project_reply, user_status, organization, SavedItem, education, post, post_comments, user_project, event, current_position, event_comment, event_reply
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.db.models import Q
# from django.contrib.postgres.search import TrigramSimilarity

# Create your views here.

#Auth:
class sign_up(View):
    def get(self, request):
        form = RegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'registration/sign_up.html', context)
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            userinfo.objects.create(user=user)
            current_position.objects.create(user = user.info)
            education.objects.create(user = user.info)
            # user.save()
            
            username = form.cleaned_data.get("username") #Authenticate the user:
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")
            user = authenticate(username = username, password=password)
            if user is not None:
                login(request, user) # Log the user in
                print(user)
                return redirect('/home')
        context = {
            'form': form
        }
        return render(request, 'registration/sign_up.html', context)
        
def index(request):
    return render(request, 'myapp/index.html') 

#profile-page
@login_required
def user_profile(request, user_name):
    # userinfo_obj = userinfo.objects.get(user__username = user_name)
    userinfo_obj = get_object_or_404(userinfo, user__username = user_name)
    user_project = user_created_project = user_post= link_available = open_exp_flag = open_edu_flag = open_editprofile_flag = open_project_flag = open_cp_flag =editprofile_form = edu_form = exp_form = project_form = skill_form = cp_form = False
    social_links = { 
    'github': userinfo_obj.github if userinfo_obj.github else None,
    'linkedin': userinfo_obj.linkedin if userinfo_obj.linkedin else None,
    'stack-overflow': userinfo_obj.stackoverflow if userinfo_obj.stackoverflow else None,
}
    if social_links.get('github') or social_links.get('linkedin') or social_links.get('stackoverflow'):
        link_available = True
    skill_list = userinfo_obj.skills.all()
    exp_obj = userinfo_obj.experiences.all().order_by('-start_date')
    post_form = PostForm()
    
    
    section = request.GET.get('section', 'overview') 
    if section == 'projects':
        project = request.GET.get('project')
        if project == 'created':
            user_created_project = userinfo_obj.created_projects.all()
        else:
            user_project = userinfo_obj.projects.all().order_by('-start_date')
            if not user_project and userinfo_obj.created_projects.all():
                redirect_url = reverse("user_profile", args=[userinfo_obj.user.username])
                return redirect(f'{redirect_url}?section=projects&project=created')
        
    if section == 'posts':
        user_post = post.objects.filter(user = userinfo_obj).order_by('-created_at')
    
    is_following = request.user.info.is_following(userinfo_obj)
    # Suggested Project
    if request.user.info.skills.all():
        suggested_project = projects.objects.filter(skill_needed__in = request.user.info.skills.all()).distinct().order_by('-created_at')[:5]
    else:
        suggested_project = projects.objects.all()[:5] #For user, with no skill
    if request.user.info == userinfo_obj:
        #Edit options
        edu_form = EditEducationForm(instance=request.user.info.education)
        exp_form = EditExperienceForm()
        editprofile_form = EditProfileForm(instance=request.user.info)
        project_form = UserProjectForm()
        skill_form = EditSkillForm()
        cp_form = EditCurrentPositionForm(instance=request.user.info.current_position)
        
        
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'experience':
            exp_form = EditExperienceForm(request.POST)
            if exp_form.is_valid():
                form = exp_form.save(commit=False)
                form.user = request.user.info
                form.save()
                exp_form = EditExperienceForm()
            else:
                open_exp_flag = True
        elif form_type == 'education':
            edu_form = EditEducationForm(request.POST, instance=request.user.info.education)
            if edu_form.is_valid():
                edu_form.save()
            else:
                open_edu_flag = True
        elif form_type == 'editprofile':
            editprofile_form = EditProfileForm(request.POST, request.FILES, instance = request.user.info)
            if editprofile_form.is_valid():
                print(request.FILES['profileImg'])
                editprofile_form.profile_image = request.FILES['profileImg']
                editprofile_form.save()
                redirect_url = reverse("user_profile", args=[request.user.username])
                return redirect(redirect_url)
            else:
                open_editprofile_flag = True
        elif form_type == 'project':
            project_form = UserProjectForm(request.POST, request.FILES)
            if project_form.is_valid():
                form = project_form.save(commit=False)
                form.user = request.user.info
                form.save()
                project_form = UserProjectForm()
                redirect_url = reverse('user_profile', args=[request.user.username])
                return redirect(f'{redirect_url}?section=projects')
            else:
                open_project_flag = True
        elif form_type ==  'current_position':
            cp_form = EditCurrentPositionForm(request.POST, instance=request.user.info.current_position)
            if cp_form.is_valid():
                form = cp_form.save()
                redirect_url = reverse('user_profile', args=[request.user.username])
                return redirect(f'{redirect_url}')       
            else: 
                open_cp_flag = True   
                
                                                                  
            
        # elif form_type == 'skill':
        #     skill_form   = EditSkillForm(request.POST)
                
    context = {
        'userinfo_obj': userinfo_obj,
        'social_links': social_links,
        'link_available': link_available,
        'skill_list': skill_list,
        'exp_obj': exp_obj,
        'section': section,
        'color': {
            'active':"bg-black px-2 md:px-4 py-2 cursor-pointer rounded-md text-white font-bold hover:bg-[white] transition hover:text-black",
            'normal':"px-2 py-2 rounded-md cursor-pointer md:px-2 hover:bg-[white] transition"
            },
        'is_following': is_following,
        'user_project': user_project,
        'user_created_project': user_created_project,
        'user_post': user_post,
        'suggested_project': suggested_project,
        'ep_form': editprofile_form,
        'edu_form': edu_form,
        'exp_form': exp_form,
        'post_form': post_form,
        'skill_form': skill_form,
        'project_form': project_form,
        'cp_form': cp_form,
        'flag': {'open_edu_flag': open_edu_flag, 'open_exp_flag': open_exp_flag, 'open_editprofile_flag': open_editprofile_flag, 'open_project_flag': open_project_flag, 'open_cp_flag': open_cp_flag}
    }
    return render(request, 'myapp/user-profile_1.html', context)

#follow request:
@login_required
def unfollow_user(request, otheruserinfo_id):
    otheruser = userinfo.objects.get(id = otheruserinfo_id)
    user = request.user.info
    if user != otheruser:
        user.unfollow(otheruser)
        return JsonResponse({"status": "unfollowed", "message": "User unfollowed Successfully.", 'followers_count': otheruser.get_followers().count(), 'following_count': otheruser.get_following().count()})
    return JsonResponse({"status":"error", "message": "Invalid request."}, status = 400)

@login_required
def follow_user(request, otheruserinfo_id):
    otheruser = userinfo.objects.get(id = otheruserinfo_id)
    user = request.user.info
    if user != otheruser:
        user.follow(otheruser)
        return JsonResponse({"status": "followed", "message": "User followed successfully.", 'followers_count': otheruser.get_followers().count(), 'following_count': otheruser.get_following().count()})
    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)
    # return redirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required
def follow_list(request, username):
        userinfo_obj = userinfo.objects.get(user__username = username) #user-profile list
        l = request.GET.get('list')
        grp = False
        if l == None:
            return HttpResponseRedirect(f'{request.path}?list=followers')
        if l == 'followers':
            list = userinfo_obj.get_followers()
        elif l == 'following':   
            list = userinfo_obj.get_following()
        elif l == 'org':
            list = userinfo_obj.followed_organization.all()
            grp = True
        
        if request.user.info.skills.all():
            suggested_project = projects.objects.filter(skill_needed__in = request.user.info.skills.all()).distinct().order_by('-created_at')[:5]
        else:
            suggested_project = projects.objects.all()[:5] #For user, with no skill
            
        print(list)
        p = Paginator(list, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        context = {
            'userinfo_obj': userinfo_obj,
            'user_list': page_obj,
            'l': l,
            'grp': grp,
            'suggested_project': suggested_project,
        }
        
        return render(request, 'myapp/followList.html', context)
    
# Organization
def create_organization(request):
    if request.method == "POST":
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            org = form.save(commit=False)
            org.user = request.user
            org.save()
            return redirect('organization_page', id=org.id)
    else:
        form = OrganizationForm()      
    context  = {'form': form}
    return render(request, 'myapp/create-org.html', context)  
        
@login_required
def explore_organization(request):
    context = {
        
    }
    return render(request, 'myapp/explore-organization.html', context)
        
@login_required
def organization_page(request, id):
    organization_obj = get_object_or_404(organization, id = id)
    link_available = False
    section = request.GET.get('section', 'overview') 
    social_links = { 
        'github': organization_obj.github if organization_obj.github else None,
        'linkedin': organization_obj.linkedin if organization_obj.linkedin else None,
        'x-twitter': organization_obj.twitter if organization_obj.twitter else None,
        'discord': organization_obj.discord if organization_obj.discord else None,
        'instagram': organization_obj.instagram if organization_obj.instagram else None
    }
    suggested_org = organization.objects.filter(industry=organization_obj.industry, organization_type=organization_obj.organization_type).exclude(Q(id=organization_obj.id) | Q(user=request.user) | Q(followers=request.user.info)).order_by('?')[:5]
    if social_links.get('github') or social_links.get('linkedin') or social_links.get('x-twitter') or social_links.get('discord') or social_links.get('instagram'):
            link_available = True
    context = {
        'organization': organization_obj,
        'section': section,
        'social_links': social_links,
        'link_available': link_available,
        'color_active' : "bg-black text-white font-bold",
        'suggested_org': suggested_org
    }
    return render(request, 'myapp/organization-profile.html', context)

@login_required
def org_follow_list(request, org_id):
    org = get_object_or_404(organization, id = org_id)
    list = org.get_followers()
    if request.user.info.skills.all():
            suggested_project = projects.objects.filter(skill_needed__in = request.user.info.skills.all()).distinct().order_by('-created_at')[:5]
    else:
        suggested_project = projects.objects.all()[:5] #For user, with no skill
    print(list)
    p = Paginator(list, 3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {
        'org': org,
        'user_list': page_obj,
        'suggested_project': suggested_project,
    }
    return render(request, 'myapp/org-followlist.html', context)


@login_required
def follow_organization(request, organization_id):
    try:
        org = organization.objects.get(id=organization_id)
        user_info = request.user.info 
        if user_info not in org.followers.all():
            org.followers.add(user_info)
            return JsonResponse({'status': 'success', 'action': 'follow', 'message': 'You are now following this organization.', 'followers_count': org.get_followers().count()})
        else:
            return JsonResponse({'status': 'error', 'message': 'You are already following this organization.'}, status=400)
    except org.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Organization not found.'}, status=404)
    
@login_required
def unfollow_organization(request, organization_id):
    try:
        org = organization.objects.get(id=organization_id)
        user_info = request.user.info
        if user_info in org.followers.all():
            org.followers.remove(user_info)
            return JsonResponse({'status': 'success', 'action': 'unfollow', 'message': 'You have unfollowed this organization.', 'followers_count': org.get_followers().count()})
        else:
            return JsonResponse({'status': 'error', 'message': 'You are not following this organization.'}, status=400)
    except org.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Organization not found.'}, status=404)

@login_required
def edit_profile(request):
    form = EditProfileForm()
    context = {
        'form': form
    }
    return render(request, 'myapp/editprofile.html', context)

#explore page:
@login_required
def explore_project(request):
    
    #filter
    domain_filter = request.GET.get('domain') #id
    type_filter = request.GET.get('type') #name
    skill_filter = request.GET.get('skill') #id
    level_filter = request.GET.get('level') #name
    filter_conditions = {}
    if domain_filter:
        filter_conditions["domain__id"] = domain_filter
    if type_filter:
        filter_conditions["type"] = type_filter
    if level_filter:
        filter_conditions["level"] = level_filter
        
    filter_project = projects.objects.filter(**filter_conditions)
    
    if skill_filter:
        filter_project = filter_project.filter(skill_needed__id = skill_filter)

    applied_filter = (domain_filter or type_filter or skill_filter or level_filter)
    
    if not applied_filter:
        filter_project = projects.objects.all()[:20]
    
    #Pagination
    p = Paginator(filter_project, 7)
    page_number = request.GET.get("page")
    post_form = PostForm()
    
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        page_obj = p.page(1)
    
    print(page_number, page_obj)
    r = filter_project.count()
    top_domain = Domain.objects.all()[:10]
    top_skill= skill.objects.all()[:10]
        
    context = {
        'filtered_project': page_obj,
        'total_result': r,
        'top_domains': top_domain,
        'types': ['Open-Source', 'Learning', 'Paid', 'Freelance'],
        'levels': ['Beginner', 'Intermediate', 'Expert'],
        'top_skill': top_skill,
        'applied_filter': applied_filter,
        'post_form': post_form
    }
    # print(request.GET)
    return render(request,"myapp/explore-projects.html", context)

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
    return render(request, 'myapp/project_detail.html', context)

@login_required
def project_detail_members(request, id):
    project = get_object_or_404(projects, id = id)
    members =  project.members.all()
    post_form = PostForm()
    
    p = Paginator(members, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    context = {
        'project': project,
        'joined_members': members,
        'post_form': post_form,
        'page_obj': page_obj,
        
    }
    return render(request, 'myapp/project-member-list.html', context)
@login_required
def project_forum(request, id):
    project = get_object_or_404(projects, id=id)
    userinfo_obj = get_object_or_404(userinfo, user=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        if not content:  # Checks if content is empty or None
            redirect_url = f"{reverse('project_detail', args=[project.id])}?comment_error=Invalid-Comment#commentsection"
            return redirect(redirect_url)
        
        parent_comment_id = request.POST.get("parent_comment_id")
        print(parent_comment_id)
        
        if parent_comment_id:
            parent_comment = get_object_or_404(project_comment, id = parent_comment_id)
            r = project_reply.objects.create(user=userinfo_obj, comment = parent_comment, content=content)
            redirect_url = f"{reverse('project_detail', args=[project.id])}#reply-{r.id}"
        else:
            c = project_comment.objects.create(user=userinfo_obj, project= project,content = content)
            redirect_url = f"{reverse('project_detail', args=[project.id])}#comment-{c.id}"

    return redirect(redirect_url)
                
@login_required
def join_project(request, id):
    project = get_object_or_404(projects, id=id)
    userinfo_obj = get_object_or_404(userinfo, user=request.user)
    
    if userinfo_obj in project.members.all():
        project.members.remove(userinfo_obj)
        joined = False
    else:
        project.members.add(userinfo_obj)
        joined = True
    return JsonResponse({"joined": joined, "total_member": project.tot_member()})

@login_required
def explore_dev(request):
    filter_dev = userinfo.objects.all().exclude(user=request.user)
    
    top_domain = Domain.objects.all()[:10]
    top_skill= skill.objects.all()[:10]
    status = user_status.objects.all()
    
    #Pagination
    p = Paginator(filter_dev, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    r = filter_dev.count()
    post_form = PostForm()
    context = {
        'filter_user': page_obj,
        'top_domains': top_domain,
        'top_skill': top_skill,
        'status': status,    
        'total_result': r,  
        'post_form': post_form,  
    }
    return render(request, 'myapp/explore_dev.html', context)

#Explore event and single page event
def explore_events(request):
    filtered_events = event.objects.all()
    post_form = PostForm()
    context = {
        'post_form': post_form,
        'filtered_event': filtered_events
    }
    return render(request, 'myapp/explore-events.html', context)

def event_detail(request, id):
    event_obj = get_object_or_404(event, pk=id)
    post_form = PostForm()
    comments = event_obj.forum.all()
    context = {
        'event_obj': event_obj,
        'post_form' : post_form,
        'comments': comments,
    }
    return render(request, 'myapp/event_detail.html', context)

def event_forum(request, id):
    Event = get_object_or_404(event, id = id)
    userinfo_obj = get_object_or_404(userinfo, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        if not content:  # Checks if content is empty or None
            redirect_url = f"{reverse('event_detail', args=[Event.id])}?comment_error=Invalid-Comment#commentsection"
            return redirect(redirect_url)
        parent_comment_id = request.POST.get("parent_comment_id")
        
        if parent_comment_id:
            parent_comment = get_object_or_404(event_comment, id = parent_comment_id)
            r = event_reply.objects.create(user=userinfo_obj, comment = parent_comment, content=content)
            redirect_url = f"{reverse('event_detail', args=[Event.id])}#reply-{r.id}"
        else:
            c = event_comment.objects.create(user=userinfo_obj, event=Event ,content = content)
            redirect_url = f"{reverse('event_detail', args=[Event.id])}#comment-{c.id}"

    return redirect(redirect_url)

def saved_page(request):
    saved_item  = request.user.info.saved_items
    saved_post = saved_item.posts.all()
    saved_project = saved_item.project.all()
    saved_event = saved_item.events.all()
    post_form = PostForm()
    print(saved_item, request.META.get('HTTP_REFERER', '/'))
    print(saved_event)
    context = {
        'saved_item': saved_item,
        'section': 'posts',
        'post_form': post_form,
        'saved_post': saved_post,
        'saved_project': saved_project,
        'saved_events': saved_event,
    }
    return render(request, 'myapp/saved.html', context)

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
def toggle_like(request, post_id):
    post_obj = get_object_or_404(post, id = post_id)
    userinfo_obj = request.user.info
    if userinfo_obj in post_obj.likes.all():
        post_obj.likes.remove(userinfo_obj)
        liked = False
    else:
        post_obj.likes.add(userinfo_obj)
        liked = True

    return JsonResponse({'liked': liked, 'total_likes': post_obj.total_likes()}) 

#for saving post
def save_post(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user = request.user.info  # Set current user's profile
        new_post.aspect = request.POST.get("aspect_ratio", "16:9")
        new_post.save()
        redirect_url = reverse('user_profile', args=[request.user.username])
        return redirect(f'{redirect_url}?section=posts')
    else:
        return HttpResponseRedirect('/home')
        
#for saving post comments
def save_comment(request):
    print(True)
    comment_text = request.POST.get('comment')   
    post_id = request.POST.get('post_id')
    print(post_id)
    Post_obj = get_object_or_404(post, id=post_id)
    
    comment = post_comments.objects.create(
        Post=Post_obj,
        user=request.user.info,
        content=comment_text
    )
    profile_image_url = comment.user.profile_image.url
    data = {
        'username': comment.user.user.username,
        'comment': comment.content,
        'created_at': comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        'profile_image_url': profile_image_url,
        'comments_count': Post_obj.tot_comments(),
    }
    return JsonResponse(data)

@login_required
def toggle_post_save(request, post_id):
    post_obj = get_object_or_404(post, id = post_id)
    saved_obj, created = SavedItem.objects.get_or_create(user=request.user.info)
    print(created)
    if post_obj in saved_obj.posts.all():
        saved_obj.posts.remove(post_obj)
        saved = False
    else:
        saved_obj.posts.add(post_obj)
        saved = True
    return JsonResponse({'saved': saved})

def logout_view(request):
    logout(request)
    return redirect("/")