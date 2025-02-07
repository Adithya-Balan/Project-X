from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from .models import project_comment, project_reply, userinfo, skill, Domain, organization

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
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=False)
    skills = forms.ModelMultipleChoiceField(
        queryset=skill.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'skills-select'}),
        required=False
    )
    domains = forms.ModelMultipleChoiceField(
        queryset=Domain.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'domains-select'}),
        required=False
    )
    class Meta:
        model = userinfo
        exclude = ['user', 'years_of_experience', 'skills', 'domains']
    field_order = ['first_name', 'last_name', '__all__']