from django import forms
from myapp.models import skill, projects
from django.core.exceptions import ValidationError

class ProjectForm(forms.ModelForm):
    MAX_FILE_SIZE = 5 * 1000 * 1000  # 5 MB 
    MAX_VIDEO_SIZE = 20 * 1000 * 1000 # 20 MB
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
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-80',
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
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            print(file.size)
            if file.size > self.MAX_FILE_SIZE:
                raise ValidationError(f'File size must not exceed 5 MB. Current size: {(file.size / 1000 / 1000):.2f} MB')
        return file

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if video.size > self.MAX_VIDEO_SIZE:
                raise ValidationError(f'Video size must not exceed 20 MB. Current size: {(video.size / 1000 / 1000):.2f} MB')
        return video