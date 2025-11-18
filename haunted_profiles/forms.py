from django import forms
from .models import User


class ProfileSetupForm(forms.ModelForm):
    """Form for setting up user profile after verification - Gen Z style!"""
    
    linkedin_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://linkedin.com/in/your-profile',
            'class': 'haunted-input'
        }),
        label='LinkedIn Profile'
    )
    
    devpost_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://devpost.com/your-username',
            'class': 'haunted-input'
        }),
        label='Devpost Profile'
    )
    
    class Meta:
        model = User
        fields = ['github_link', 'ghost_avatar']
        widgets = {
            'github_link': forms.URLInput(attrs={
                'placeholder': 'https://github.com/your-username',
                'class': 'haunted-input'
            }),
        }
        labels = {
            'github_link': 'GitHub Profile',
            'ghost_avatar': 'Your Ghost Avatar',
        }
        help_texts = {
            'ghost_avatar': 'Upload your spooky avatar 👻',
        }
