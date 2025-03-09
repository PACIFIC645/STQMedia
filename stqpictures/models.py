from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image  # Image optimization
import os
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/', default='profiles/default.jpg')
    bio = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize image to optimize storage
        if self.profile_picture:
            img_path = self.profile_picture.path
            img = Image.open(img_path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(img_path)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='images/blog/', null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)  # Stores uploaded videos
    youtube_url = models.URLField(blank=True, null=True)  # Stores YouTube links
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)  # Tracks who uploaded

    def clean(self):
        """Ensure at least one of YouTube URL or uploaded video is provided."""
        if not self.youtube_url and not self.video_file:
            raise ValidationError("Either a YouTube URL or an uploaded video is required.")
        
        if self.youtube_url and self.video_file:
            raise ValidationError("Provide either a YouTube URL or upload a video, not both.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price in ZAR
    image = models.ImageField(upload_to='images/products/', null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)  # Optional: categorize products
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price in ZAR
    duration = models.DurationField(null=True, blank=True)
    service_type = models.CharField(max_length=100, blank=True)  # Optional: categorize services
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)  # For products
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.CASCADE)  # For services
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'product', 'service')

    def __str__(self):
        if self.product:
            return f'{self.product.name} (x{self.quantity})'
        elif self.service:
            return f'{self.service.name} (x{self.quantity})'
        return 'CartItem'
    

class CompetitionEntry(models.Model):
    CATEGORY_CHOICES = [
        ("music_video", "Music Video"),
        ("documentary", "Documentary"),
        ("motivation", "Motivation"),
        ("films", "Films"),
        ("craft", "Craft"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="music_video")
    upload_link = models.URLField()
    submission_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)  # Only active competitions can be entered

    def __str__(self):
        return f"{self.name} - {self.category}"

    @staticmethod
    def get_active_competition():
        """Ensure only the Music Video Competition is active"""
        return CompetitionEntry.objects.filter(category="music_video", active=True)
