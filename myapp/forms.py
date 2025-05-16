from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from .models import project_comment, project_reply, userinfo, skill, Domain, organization, education, experience, post, user_project, event, current_position, projects
from django.forms.widgets import ClearableFileInput
# from django_select2.forms import Select2MultipleWidget
class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = ''
    initial_text = ''
    input_text = 'Change'
    template_name = 'widgets/custom_file_input.html'  # Optional for more customization

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields =  ["first_name", "last_name", "username", "email", "password1", "password2"]
    
        help_texts = {
            'username': "Enter Unique Username"
        }
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_valid = username[0].isalpha() and bool(re.match(r'^[a-zA-Z0-9_.]+$', username)) and username.count('.') <= 1  and '..' not in username
        if is_valid==False:
            raise forms.ValidationError("Username must start with a letter and contain only letters, numbers, underscore and dot")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email == None or email == "":
            raise forms.ValidationError("Email Should not be Empty")
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already Exists.")
        return email
    
class Postsignup_infoForm(forms.ModelForm):
    class Meta:
        model = userinfo
        fields = ['status', 'availability', 'cringe_badge']
        widgets = {
            'availability': forms.Select(attrs={
                'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'cringe_badge': forms.Select(attrs={
                'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent'
            }),
        }
    

class OrganizationForm(forms.ModelForm):
    founded_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = organization
        exclude = ['user', 'followers']

        widgets = {
            'logo': forms.ClearableFileInput(attrs={
                'class': 'border border-gray-700 p-2 rounded-lg w-full file:bg-black file:text-white file:border-none file:px-4 file:py-2 file:rounded-lg cursor-pointer'
            },),
            "name": forms.TextInput(attrs={"placeholder": "Enter organization name"}),
            "description": forms.Textarea(attrs={"placeholder": "Enter a brief description about your organization"}),
            "phone": forms.TextInput(attrs={'type': 'tel', "placeholder": "Enter phone number (e.g., +1 234 567 890)"}),
            "website": forms.URLInput(attrs={"placeholder": "organization website URL (if any)"}),
            "linkedin": forms.URLInput(attrs={"placeholder": "https://www.linkedin.com/company/organization-name"}),
            "github": forms.URLInput(attrs={"placeholder": "https://github.com/organization-name"}),
            "twitter": forms.URLInput(attrs={"placeholder": "https://twitter.com/organization-handle"}),
            "location": forms.TextInput(attrs={"placeholder": "Enter headquarters location (City, Country)"}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            "instagram": forms.URLInput(attrs={"placeholder": "https://www.instagram.com/organization-name"}),
            "discord": forms.URLInput(attrs={"placeholder": "https://discord.com/invite/organization-link"}),
        }

class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = project_comment
        fields = ['content']
        
class ProjectReplyForm(forms.ModelForm):
    class Meta:
        model = project_reply
        fields = ['content']
        
class EditOrgForm(forms.ModelForm):
    
    class Meta:
        model = organization
        exclude = ['user', 'followers']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Organization Name'}),
            'description': forms.Textarea(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Description...', 'rows': 8}),
            'website': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'www.samplesite.com'}),
            'industry': forms.Select(attrs={'class': 'outline-none border border-black px-2 py-1 bg-white'}),
            'location': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Location'}),
            'organization_type': forms.Select(attrs={'class': 'outline-none border border-black px-2 py-1 bg-white'}),
            'founded_date': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1'}),
            'contact_email': forms.EmailInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'type': 'tel', 'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Phone'}),
            'github': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Github URL'}),
            'linkedin': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'LinkedIn URL'}),
            'instagram': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Instagram URL'}),
            'twitter': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Twitter URL'}),
            'discord': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Discord URL'}),
            'logo': forms.ClearableFileInput(attrs={'id': 'imgInput','class': 'hidden'}),
        }


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'First'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Last'}))
    username = forms.CharField(max_length = 50, required=True, widget=forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Username'}))
    
    class Meta:
        model = userinfo
        exclude = ['user', 'years_of_experience', 'skills', 'domains', 'profile_views']
        
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Bio...'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1', 'id':"dob"}),
            'location': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Location'}),
            'contact_email': forms.EmailInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'type': 'tel','class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Phone'}),
            'gender': forms.Select(attrs={'class': 'outline-none border border-black px-2 py-1 bg-white', }),
            'availability': forms.Select(attrs={'class': 'outline-none border border-black px-2 py-1 bg-white', }),
            'status': forms.Select(attrs={'class': 'outline-none border border-black px-2 py-1 bg-white', }),
            'website': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'www.samplesite.in'}),
            'linkedin': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Linkedin URL'}),
            'github': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Github URL'}),
            'stackoverflow': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Stackoverflow URL'}),
            'profile_image': forms.ClearableFileInput(attrs={'id': 'imgInput','class': 'hidden'}),
            'cringe_badge': forms.Select(attrs={'class': 'outline-none border border-black px-2 py-1 bg-white'})
        }
        labels = {
            'bio': ' Tagline (Short Bio)',
            'contact_email': 'Contact Email (If any)',
        }
        
    
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            user = self.instance.user
            self.fields['first_name'].initial =  user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['username'].initial = user.username
            
    def clean_username(self):
        """
        Validates the username field to ensure it:
          - Starts with a letter.
          - Contains only letters, numbers, underscore, and dot.
          - Has at most one dot.
          - Does not contain consecutive dots.
        """
        username = self.cleaned_data.get("username")
        if username:
            is_valid = (
                username[0].isalpha() and
                bool(re.match(r'^[a-zA-Z0-9_.]+$', username)) and
                username.count('.') <= 1 and
                '..' not in username
            )
            if not is_valid:
                raise forms.ValidationError(
                    "Username must start with a letter and contain only letters, numbers, underscores, and a single dot (with no consecutive dots)."
                )

            qs = User.objects.filter(username=username)
            if self.instance.user:
                qs = qs.exclude(pk=self.instance.user.pk)
            if qs.exists():
                raise forms.ValidationError("This username is already taken.")
        return username
            
    def save(self,commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        
        user.full_clean()
        user.save()
        instance = super(EditProfileForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    
class EditEducationForm(forms.ModelForm):
    start_date = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'outline-none border border-black px-2 py-1'})
    )
    end_date = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'outline-none border border-black px-2 py-1'})
    )
    class Meta:
        model = education
        exclude = ['user']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Eg: Harvard University'}),
            'field_of_study': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Eg: Computer Science'}),
            'degree': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Eg: B.Tech'}),
            # 'start_date': forms.DateInput(attrs={'type': 'month', 'class': 'outline-none border border-black px-2 py-1'}),
            # 'end_date': forms.DateInput(attrs={'type': 'month', 'class': 'outline-none border border-black px-2 py-1', 'id':"endDate"}),
        }                                                               
        labels = {
            'name': 'University Name',
            'field_of_study': 'Course',
            'till_now': 'Currently Pursuing',
            'end_date': 'End date (or expected)',
        }
        error_messages = {
            'name': {'required':'University name is required',},
            'field_of_study': {'required': 'Enter a Valid course',}
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format initial value to 'YYYY-MM' if data exists
        if self.instance and self.instance.start_date:
            self.initial['start_date'] = self.instance.start_date.strftime('%Y-%m')
        if self.instance and self.instance.end_date:
            self.initial['end_date'] = self.instance.end_date.strftime('%Y-%m')
            
    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")
        print(start_date)
        if start_date:
            return datetime.strptime(start_date, "%Y-%m").date().replace(day=1)  # Convert YYYY-MM to YYYY-MM-01
        return None

    def clean_end_date(self):
        end_date = self.cleaned_data.get("end_date")
        if end_date:
            return datetime.strptime(end_date, "%Y-%m").date().replace(day=1)  # Convert YYYY-MM to YYYY-MM-01
        return None
        
class UserProjectForm(forms.ModelForm):
    class Meta:
        model = user_project
        exclude = ['user', 'techstack']
        labels = {
            'name': 'Project Name',
            'description': 'Description',
            'url': 'URL (If any)',
            'repo_link': 'Github-URL (If any)',
            'end_date': "End Date",
            'media': 'Thumbnail'
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Project Name'}),
            'description': forms.Textarea(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Tell More about your Project'}),
            'url': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder':'https://livedemo.in/'}),
            'repo_link': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'https://github.com/project-x'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1'}),
            'media': forms.ClearableFileInput(attrs={'class': 'border border-gray-700 p-2 rounded-lg w-full file:bg-black file:text-white file:border-none file:px-4 file:py-2 file:rounded-lg cursor-pointer'})
        }
        
class EditCurrentPositionForm(forms.ModelForm):
    start_date = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'outline-none border border-black px-2 py-1'})
    )
    end_date = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'outline-none border border-black px-2 py-1'})
    )
    class Meta:
        model = current_position
        exclude = ['user']
        labels = {
            'name': 'Enter your Current Position',
            'role': 'Enter your Role',
            'description': 'Explain Your Role',
            'till_now': 'Currently Working',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Company Name'}),               
            'role': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Role'}),      
            'description': forms.Textarea(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Briefly Describe your Role.'}),
            # 'start_date': forms.DateInput(attrs={'type': 'month', 'class': 'outline-none border border-black px-2 py-1'}),
            # 'end_date': forms.DateInput(attrs={'type': 'month', 'class': 'outline-none border border-black px-2 py-1', 'id':"endDate"}),                       
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format initial value to 'YYYY-MM' if data exists
        if self.instance and self.instance.start_date:
            self.initial['start_date'] = self.instance.start_date.strftime('%Y-%m')
        if self.instance and self.instance.end_date:
            self.initial['end_date'] = self.instance.end_date.strftime('%Y-%m')
            
    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")
        print(start_date)
        if start_date:
            return datetime.strptime(start_date, "%Y-%m").date().replace(day=1)  # Convert YYYY-MM to YYYY-MM-01
        return None

    def clean_end_date(self):
        end_date = self.cleaned_data.get("end_date")
        if end_date:
            return datetime.strptime(end_date, "%Y-%m").date().replace(day=1)  # Convert YYYY-MM to YYYY-MM-01
        return None

class EditExperienceForm(forms.ModelForm):
    class Meta:
        model = experience
        exclude = ['user']
        labels = {
            'name': 'Company/Organization',
            'till_now': 'Currently Working',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Company Name'}),
            'role': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Role'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1', 'id':"endDate"}),
        }
        error_messages = {
            'name': {'required':'Company name is required',},
            'role': {'required': 'Enter a Valid role',}
        }

class EditSkillForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=skill.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2 w-full ',
            'id': 'mySelect',
        }),
        required=False,
    )
    class Meta:
        model = userinfo
        fields = ('skills',)
        
class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['file', 'content']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'hidden',
                'id': 'uploadPost',
                'name': 'post',
            }),
            'content': forms.Textarea(attrs={
                'class': 'text-gray-700 w-full h-36 outline-none resize-none',
                'placeholder': 'Content....'
            }),
        }
        
class EventForm(forms.ModelForm):
    class Meta:
        model = event
        exclude = ['organization', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Event Title',
                'id': 'eventName'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-20',
                'placeholder': 'Event Description',
                'id': 'eventShortDescription'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-80',
                'placeholder': 'Give a Brief Overview of the Event, details, rewards...',
                'id': 'eventDescription'
            }),
            'event_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'id': 'eventType'
            }),
            'mode': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 bg-white',
                'id': 'eventMode'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Location',
                'id': 'eventLocation',
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 bg-white',
                'id': 'eventStartdate'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 bg-white',
                'id': 'eventStartTime',
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 bg-white',
                'id': 'eventEnddate'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 bg-white',
                'id': 'eventEndTime',
            }),
            'registration_link': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'https://register-link.com',
                'id': 'regLink'
            }),
            'contact_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Organizer Name',
                'id': 'eventOrganizerName'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Organizer Email',
                'id': 'eventOrganizerEmail'
            }),
            'contact_phone': forms.TextInput(attrs={
                'type': 'tel',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Organizer Phone',
                'id': 'eventOrganizerPhone'
            }),
            'banner': forms.FileInput(attrs={
                'class': 'w-full border border-gray-300 p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 file:bg-black file:text-white file:border-none file:px-4 file:py-2 file:rounded-md file:cursor-pointer hover:file:bg-[#d2d2d2] hover:file:text-black transition'
            }),
        }
        labels = {
            'title': 'Event Name',
            'start_time':'Event Time'
        }
    
class ProjectForm(forms.ModelForm):
    skill_needed = forms.ModelMultipleChoiceField(
        queryset=skill.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2 w-full h-16 px-4 py-2 outline-none border border-gray-300 rounded-md focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all duration-200 text-gray-800',
            'id': 'mySelect',
        }),
        required=True,
    )
    class Meta:
        model = projects
        exclude = ['creator', 'members', 'created_at']
        labels = {
            'title': 'Project Name',
            'description': 'Description',
            'image': 'Thumbnail/Banner',
            'url': 'Demo URL',
            'github_link': 'Github-URL',
            'skill_needed': "Required Skills",
            'video': "Demo Video (If Any)",
            'file': "Documentation (PDF, DOCX, PPT)",
        }
        help_texts = {
            'image': 'Upload an image that represents your project',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Project Title',
                'id': 'projectTitle'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-40',
                'placeholder': 'Briefly describe your project, requirements and timeline.',
                'id': 'projectDescription'
            }),
            'level': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 bg-white',
                'id': 'projectLevel'
            }),
           
            'github_link': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'https://github.com/project',
                'id': 'regLink'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'https://project-demo.com',
                'id': 'projectUrl'
            }),
            'type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'id': 'projectType'
            }),
            'domain': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 bg-white',
                'placeholder': 'Select Domain relevant to Your Project',
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full border border-gray-300 p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 file:bg-black file:text-white file:border-none file:px-4 file:py-2 file:rounded-md file:cursor-pointer hover:file:bg-[#d2d2d2] hover:file:text-black transition'
            }),
            'file': forms.FileInput(attrs={
                'class': 'hidden',  # Hide the default file input
            }),
            'video': forms.FileInput(attrs={
                'class': 'hidden',  # Hide the default file input
                'accept': 'video/*',  # Accept only video files
            }),
            
        }