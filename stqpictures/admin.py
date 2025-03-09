from django.contrib import admin
from django.utils.html import format_html  # ✅ For image thumbnails
from .models import BlogPost, Video, Profile  # ✅ Import all models

# ✅ BlogPost Admin Configuration
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    search_fields = ('title',)

# ✅ Video Admin Configuration
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_file', 'youtube_url')

# ✅ Profile Admin Configuration
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture_thumbnail', 'bio')
    list_display_links = ('user',)  # Makes the "user" field clickable
    list_filter = ('user__is_active', 'user__is_staff')  # Filters for active/staff users
    search_fields = ('user__username',)  # Search by username

    def profile_picture_thumbnail(self, obj):
        """Displays a circular thumbnail for the profile picture in the admin panel."""
        if obj.profile_picture and obj.profile_picture.url:
            return format_html(
                f'<img src="{obj.profile_picture.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;">'
            )
        return "No Picture"
    
    profile_picture_thumbnail.short_description = "Profile Picture"  # ✅ Set column name
