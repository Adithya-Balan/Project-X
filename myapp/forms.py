from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from .models import project_comment, project_reply, userinfo, skill, Domain, organization, education, experience, post, user_project, event, current_position
# from django_select2.forms import Select2MultipleWidget

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
    

class OrganizationForm(forms.ModelForm):
    founded_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = organization
        exclude = ['user', 'followers']
    
        help_texts = {
            'name': "Organization Name",
            # ''
        }
        widgets = {
            'logo': forms.ClearableFileInput(attrs={
                'class': 'border border-gray-700 p-2 rounded-lg w-full file:bg-black file:text-white file:border-none file:px-4 file:py-2 file:rounded-lg cursor-pointer'
            })
        }
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        if not phone:
            return phone 
        
        # Ensure length is between 10 and 14
        if not (10 <= len(phone) <= 14):
            raise forms.ValidationError("Phone number must be between 10 and 14 digits.")

        # Check if phone number contains only digits, allowing an optional leading '+'
        if not re.match(r'^\+?[0-9]+$', phone):
            raise forms.ValidationError("Phone number can only contain digits and an optional leading '+'.")

        # Ensure it starts correctly (either '+' for international or a valid starting digit)
        if phone.startswith('+'):
            if len(phone) < 11:  # Example: "+91XXXXXXXXXX"
                raise forms.ValidationError("Invalid international phone number.")
        elif not phone[0].isdigit() or phone[0] in "012345":
            raise forms.ValidationError("Phone number must start with a valid digit (6-9 for India).")

        return phone
class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = project_comment
        fields = ['content']
        
class ProjectReplyForm(forms.ModelForm):
    class Meta:
        model = project_reply
        fields = ['content']
        

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'First'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Last'}))
    username = forms.CharField(max_length = 50, required=True, widget=forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Username'}))
    
    class Meta:
        model = userinfo
        exclude = ['user', 'years_of_experience', 'skills', 'domains']
        
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Bio...'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1', 'id':"dob"}),
            'location': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Location'}),
            'contact_email': forms.EmailInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'type': 'tel','class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Phone'}),
            'gender': forms.Select(attrs={'class': 'outline-none border border-black px-2 py-1 bg-white', }),
            'status': forms.Select(attrs={'class': 'outline-none border border-black px-2 py-1 bg-white', }),
            'website': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'www.samplesite.in'}),
            'linkedin': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Linkedin URL'}),
            'github': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Github URL'}),
            'stackoverflow': forms.URLInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Stackoverflow URL'}),
            'profile_image': forms.ClearableFileInput(attrs={'id': 'imgInput','class': 'hidden'})
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
    class Meta:
        model = education
        exclude = ['user']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Eg: Harvard University'}),
            'field_of_study': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Eg: Computer Science'}),
            'degree': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Eg: B.Tech'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1', 'id':"endDate"}),
            'till_now': forms.CheckboxInput(attrs={'id': 'presentDate'}),
        }                                                               
        labels = {
            'name': 'University Name',
            'field_of_study': 'Course',
            'till_now': 'Currently Pursuing',
        }
        error_messages = {
            'name': {'required':'University name is required',},
            'field_of_study': {'required': 'Enter a Valid course',}
        }
        def clean(self):
            cleaned_data = super().clean()
            present = cleaned_data.get('till_now')
            if present:
                cleaned_data['end_date'] = None
            return cleaned_data

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
    class Meta:
        model = current_position
        exclude = ['user']
        labels = {
            'name': 'Enter your Current Position',
            'role': 'Enter your Role',
            'description': 'Explain Your Role',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Company Name'}),               
            'role': forms.TextInput(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Role'}),      
            'description': forms.Textarea(attrs={'class': 'outline-none border border-black px-2 py-1', 'placeholder': 'Briefly Describe your Role.'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'outline-none border border-black px-2 py-1', 'id':"endDate"}),                       
        }
        
    def clean(self):
        cleaned_data = super().clean()
        present = cleaned_data.get('till_now')
        if present:
            cleaned_data['end_date'] = None
        return cleaned_data

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
            'till_now': forms.CheckboxInput(attrs={'id': 'presentDate'}),
        }
        error_messages = {
            'name': {'required':'Company name is required',},
            'role': {'required': 'Enter a Valid role',}
        }
        
    def clean(self):
        cleaned_data = super().clean()
        present = cleaned_data.get('till_now')
        if present:
            cleaned_data['end_date'] = None
        return cleaned_data

class EditSkillForm(forms.ModelForm):
    class Meta:
        model = userinfo
        fields = ('skills',)
        widgets = {
            'skills': forms.SelectMultiple(attrs={
                'class': 'w-full p-2 border border-black bg-white text-black rounded'
            })
        }
        
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
        exclude = ['organization']

        
# skills = forms.ModelMultipleChoiceField(
    #     queryset=skill.objects.all(),
    #     widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'skills-select'}),
    #     required=False
    # )
    # domains = forms.ModelMultipleChoiceField(
    #     queryset=Domain.objects.all(),
    #     widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'domains-select'}),
    #     required=False
    # )