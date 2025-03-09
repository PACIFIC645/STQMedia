from django import forms
from .models import Video
from PIL import Image
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
import os
from django.contrib.auth.forms import UserCreationForm

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'youtube_url', 'video_file']  # Allow both file and URL uploads

    def clean(self):
        """Ensure at least one of YouTube URL or uploaded video is provided."""
        cleaned_data = super().clean()
        youtube_url = cleaned_data.get('youtube_url')
        video_file = cleaned_data.get('video_file')

        if not youtube_url and not video_file:
            raise forms.ValidationError("You must provide either a YouTube URL or upload a video.")
        if youtube_url and video_file:
            raise forms.ValidationError("Choose only one: YouTube URL or file upload.")

        return cleaned_data


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")
        return cleaned_data
    

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        help_texts = {
            'profile_picture': 'Upload a profile image (JPEG, PNG). Max size: 2MB.',
        }

    def clean_profile_picture(self):
        image = self.cleaned_data.get('profile_picture', False)
        
        if image:
            # Check file size (2MB limit)
            if image.size > 2 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 2MB )")
    
            # Check file type
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise ValidationError("Only JPEG and PNG images are allowed")
    
            # Validate file extension
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError("Unsupported file extension. Only .jpg, .jpeg, and .png are allowed")
    
            # Verify Image Integrity
            try:
                img = Image.open(image)
                img.verify()  # Ensure it's a valid image
            except Exception:
                raise ValidationError("Invalid image file. Please upload a valid image.")
    
        return image