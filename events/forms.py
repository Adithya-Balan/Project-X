from django import forms
from tinymce.widgets import TinyMCE
from myapp.models import event

class EventForm(forms.ModelForm):          
    description = forms.CharField(widget=TinyMCE(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 h-80',
                'placeholder': 'Give a Brief Overview of the Event, details, rewards...',
                'id': 'eventDescription'
            }))
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