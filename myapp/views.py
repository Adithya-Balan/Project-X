from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.views import View
from .forms import RegistrationForm, ProjectCommentForm, ProjectReplyForm
from django.contrib.auth.models import User
from .models import userinfo, projects, Domain, skill, project_comment, project_reply
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
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
def user_profile(request, username):
    try:
        userinfo_obj = userinfo.objects.get(user__username = username)
        user_project = link_available = False
        social_links = { 
        'github': userinfo_obj.github if userinfo_obj.github else None,
        'linkedin': userinfo_obj.linkedin if userinfo_obj.linkedin else None,
        'stack-overflow': userinfo_obj.stackoverflow if userinfo_obj.stackoverflow else None,
    }
        if social_links.get('github') or social_links.get('linkedin') or social_links.get('stackoverflow'):
            link_available = True
        skill_list = userinfo_obj.skills.all()
        exp_obj = userinfo_obj.experiences.all().order_by('-start_date')
        
        section = request.GET.get('section', 'overview') 
        if section == 'projects':
            user_project = userinfo_obj.projects.all().order_by('-start_date')
        is_following = request.user.info.is_following(userinfo_obj)
        
        # Suggested Project
        suggested_project = projects.objects.filter(skill_needed__in = request.user.info.skills.all()).distinct().order_by('-created_at')[:5]
        
        context = {
            'userinfo_obj': userinfo_obj,
            'social_links': social_links,
            'link_available': link_available,
            'skill_list': skill_list,
            'exp_obj': exp_obj,
            'section': section,
            'color': {
                'active':"bg-[#6feb8631] px-3 md:px-4 py-2 rounded-md text-[#6feb85] font-bold border border-[#6feb85] cursor-pointer",
                'normal':"px-3 py-2 rounded-md cursor-pointer md:px-4 hover:bg-[#6feb8631] hover:text-[#6feb85] border border-white hover:border hover:border-[#6feb85]"
                },
            'is_following': is_following,
            'user_project': user_project,
            'suggested_project': suggested_project,
        }
        
        return render(request, 'myapp/user-profile_1.html', context)
        
    except userinfo_obj.DoesNotExist:
        raise Http404("User information does not exist")

#follow request:
def unfollow_user(request, otheruserinfo_id):
    otheruser = userinfo.objects.get(id = otheruserinfo_id)
    user = request.user.info
    if user != otheruser:
        user.unfollow(otheruser)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def follow_user(request, otheruserinfo_id):
    otheruser = userinfo.objects.get(id = otheruserinfo_id)
    user = request.user.info
    if user != otheruser:
        user.follow(otheruser)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def follow_list(request, username):
        userinfo_obj = userinfo.objects.get(user__username = username) #user-profile list
        l = request.GET.get('list')
        
        if l == None:
            return HttpResponseRedirect(f'{request.path}?list=followers')
        if l == 'followers':
            list = userinfo_obj.get_followers()
        elif l == 'following':   
            list = userinfo_obj.get_following()
        print(list)
        p = Paginator(list, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        context = {
            'userinfo_obj': userinfo_obj,
            'user_list': page_obj,
            'l': l
        }
        
        return render(request, 'myapp/followList.html', context)

#explore page:
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
    page_obj = p.get_page(page_number)
    
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
        'applied_filter': applied_filter
    }
    # print(request.GET)
    return render(request,"myapp/explore-projects.html", context)

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

    context = {
        'project': project,
        'skill_needed': project.skill_needed.all(),
        'link_available': link_available,
        'social_link': social_links,
        'comments': comments
    }
    return render(request, 'myapp/project_detail.html', context)

def project_forum(request, id):
    project = get_object_or_404(projects, id=id)
    userinfo_obj = get_object_or_404(userinfo, user=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content')
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

def explore_dev(request):
    filter_dev = userinfo.objects.all().exclude(user=request.user)
    context = {
        'filter_user': filter_dev
    }
    return render(request, 'myapp/explore_dev.html', context)

def logout_view(request):
    logout(request)
    return redirect("/")