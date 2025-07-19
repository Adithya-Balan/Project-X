from django import forms
from .models import MindLog

class MindLogForm(forms.ModelForm):
    latency = forms.IntegerField(
    min_value=30,  # match your widget's min
    widget=forms.NumberInput(attrs={
        'type': 'range',
        'min': '30',
        'max': '999',
        'value': '180',
        'id': 'latencyRange',
        'class': 'w-full mt-1'
    }))

    class Meta:
        model = MindLog
        fields = ['content', 'neuro_color', 'latency', 'snap_shot']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': "What are you working on today?",
                'id': "mind-log-input",
                'class': "flex-1 h-12 sm:h-14 bg-transparent focus:outline-none text-white placeholder-gray-500 font-mono text-base sm:text-lg",
                'autocomplete': "off",
                'autocorrect': "off",
                'spellcheck': "false",
                'maxlength': '280',
            }),
            'neuro_color': forms.HiddenInput(attrs={
                'id': 'selectedColor',
                'name': 'selected_color'
            }),
            'snap_shot': forms.ClearableFileInput(attrs={
                'id': 'snapshotInput',
                'accept': 'image/*',
                'onchange': 'handle_log_ImageUpload(event)',
                'class': 'hidden',
            }),
        }
