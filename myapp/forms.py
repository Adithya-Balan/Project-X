from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from .models import project_comment, project_reply

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
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already Exists.")
        return email
    
class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = project_comment
        fields = ['content']
        
class ProjectReplyForm(forms.ModelForm):
    class Meta:
        model = project_reply
        fields = ['content']
        


        
        