# Core Django imports
from django.urls import path, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.contrib import messages

# Django Authentication
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

# Django Class-Based Views
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
    View,
    UpdateView,
)

# Third-Party and Utility Imports
import requests
import json
import os
import random
from stqpictures.utils import CurrencyConverter

# Project-Specific Imports
from .models import BlogPost, Product, Service, Cart, CompetitionEntry, Video, Profile
from .forms import UserRegistrationForm, ProfileUpdateForm, VideoForm


class GalleryImagesMixin:
    """Provides a DRY method to fetch gallery images from our static folder."""
    def get_gallery_images(self, count=None):
        # Build the absolute path to the gallery folder
        gallery_path = os.path.join(settings.BASE_DIR, "stqpictures", "static", "gallery")
        if os.path.exists(gallery_path):
            all_images = [
                img for img in os.listdir(gallery_path)
                if img.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))
            ]
        else:
            all_images = []
        # Return a random sample if a count is specified; otherwise return sorted list
        if count:
            return random.sample(all_images, min(len(all_images), count))
        return sorted(all_images)

class IndexView(GalleryImagesMixin, TemplateView):
    template_name = 'stqpictures/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add products, etc.
        context['products'] = Product.objects.all()
        # Add gallery preview images (6 random images)
        context['preview_images'] = self.get_gallery_images(count=6)
        return context

class GalleryView(GalleryImagesMixin, TemplateView):
    template_name = "stqpictures/gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For full gallery, list all images (sorted)
        context["images"] = self.get_gallery_images()
        return context

class GalleryPreviewView(GalleryImagesMixin, TemplateView):
    template_name = "stqpictures/includes/gallery_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For the dedicated preview view (if needed separately), only 6 images
        context["images"] = self.get_gallery_images(count=6)
        return context


# About page
class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'stqpictures/about.html')


# Mzansi page
class MzansiView(View):
    def get(self, request, *args, **kwargs):
        range_mzansi = range(1, 17)
        return render(request, 'stqpictures/mzansi.html', {'range_mzansi': range_mzansi})

# Nature page
class NatureView(View):
    def get(self, request, *args, **kwargs):
        range_nature = range(1, 9)
        return render(request, 'stqpictures/nature.html', {'range_nature': range_nature})

# Blog List View
class BlogListView(View):
    def get(self, request, *args, **kwargs):
        blog_posts = BlogPost.objects.all().order_by('-published_date')  # Retrieve all blog posts
        return render(request, 'stqpictures/blog.html', {'blog_posts': blog_posts})

# Blog Detail View
class BlogDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        blog_post = get_object_or_404(BlogPost, pk=pk)  # Retrieve a blog post by primary key
        return render(request, 'stqpictures/blog_detail.html', {'blog_post': blog_post})


# Contact page
class ContactView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'stqpictures/contact.html')


# Registration Page 
class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'stqpictures/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Automatically create Profile
            login(request, user)  # Log in the user upon successful registration
            messages.success(request, "Registration successful! Welcome to your profile.")
            return redirect('stqpictures:profile')  # Redirect to Profile
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
        return render(request, 'stqpictures/register.html', {'form': form})


# Profile View (Read-Only) displays user details (for unauthenticated users only)
class UserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'stqpictures/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # If viewing own profile
        if hasattr(self.request.user, 'profile'):
            return self.request.user.profile
        else:
            messages.error(self.request, "Profile not found. Redirecting to home.")
            return redirect('stqpictures:home')

        
# Profile Update View
class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)
        return render(request, 'stqpictures/profile_update.html', {
            'profile_form': profile_form,
            'password_form': password_form,
        })

    def post(self, request):
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        updated = False

        if profile_form.is_valid():
            profile_form.save()
            updated = True
            messages.success(request, "Profile updated successfully!")

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Keep user logged in
            updated = True
            messages.success(request, "Password updated successfully!")

        if not updated:
            messages.error(request, "Update failed. Please correct the errors below.")

        return render(request, 'stqpictures/profile_update.html', {
            'profile_form': profile_form,
            'password_form': password_form,
        })

# Profile Picture Update View (Focused on Picture Only)
class ProfilePictureUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['profile_picture']
    template_name = 'stqpictures/profile_picture_update.html'
    success_url = reverse_lazy('stqpictures:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile  # Access logged-in user's profile

    def form_valid(self, form):
        messages.success(self.request, "Profile picture updated successfully!")
        return super().form_valid(form)


# Login page (for unauthenticated users only)
class CustomLoginView(LoginView):
    template_name = 'stqpictures/login.html'  # Use your custom login template
    redirect_authenticated_user = True  # Prevent logged-in users from accessing the login page
    success_url = reverse_lazy('stqpictures:home')  # Redirect to home after successful login

    def get_success_url(self):
        """
        Override this method to ensure the user is always redirected to the `success_url`
        and not to `/accounts/profile/`.
        """
        next_url = self.request.GET.get('next')  # Check for 'next' parameter
        return next_url if next_url else self.success_url

    def form_invalid(self, form):
        """
        Handle invalid form submissions (e.g., incorrect credentials).
        Add a custom error message to the context.
        """
        return self.render_to_response(
            self.get_context_data(form=form, error='Invalid username or password')
        )


# Logout view
class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('stqpictures:home')  # Redirect to home after logout

# Checkout page (for authenticated users only)
class CheckoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return redirect('stqpictures:cart')

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'stqpictures/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

# Guest Checkout (for unauthenticated users only)
class GuestCheckoutView(View):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        cart_items = []
        
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            cart_items.append({'product': product, 'quantity': quantity})

        total_price = sum(item['product'].price * item['quantity'] for item in cart_items) if cart_items else 0

        return render(request, 'stqpictures/guest_checkout.html', {'cart_items': cart_items, 'total_price': total_price})
    

# Save for later
class SaveForLaterView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'stqpictures/save_for_later.html')

   
# Cart Views 
class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
        else:
            cart = request.session.get('cart', {})  # Retrieve guest cart from session
            cart_items = []
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)
                cart_items.append({'product': product, 'quantity': quantity})

        total_price = sum(item['product'].price * item['quantity'] for item in cart_items) if cart_items else 0

        return render(request, 'stqpictures/cart.html', {'cart_items': cart_items, 'total_price': total_price})
    

# Add to Cart View (handling both Products and Services)
class AddToCartView(View):
    def post(self, request, item_id, item_type):
        if request.user.is_authenticated:
            # Authenticated user: Add to database cart
            if item_type == "product":
                item = get_object_or_404(Product, id=item_id)
                cart, created = Cart.objects.get_or_create(user=request.user, product=item)
            elif item_type == "service":
                item = get_object_or_404(Service, id=item_id)
                cart, created = Cart.objects.get_or_create(user=request.user, service=item)
            else:
                return JsonResponse({"success": False, "message": "Invalid item type."}, status=400)

            cart.quantity += 1
            cart.save()
        else:
            # Guest User: Store in session-based cart
            cart = request.session.get('cart', {})
            if str(item_id) in cart:
                cart[str(item_id)] += 1
            else:
                cart[str(item_id)] = 1

            request.session['cart'] = cart
            request.session.modified = True

        return JsonResponse({"success": True, "message": f"Item added to cart!"})
    

# CentralView to consolidate all the views
class CentralView(View):
    def get(self, request, page_name="home", *args, **kwargs):
        # Define navigation menus
        secondary_nav_pages = ['home', 'about', 'contact', 'gallery', 'blog', 'mzansi', 'nature', 'services', 'products']

        primary_nav = [
            {'name': 'Home', 'url': 'stqpictures:home'},
            {'name': 'About', 'url': 'stqpictures:about'},
            {'name': 'Gallery', 'url': 'stqpictures:gallery'},
            {'name': 'Blog', 'url': 'stqpictures:blog_list'},
            {'name': 'Contact', 'url': 'stqpictures:contact'},
            {'name': 'Services', 'url': 'stqpictures:service_list'},
        ]

        if request.user.is_authenticated:
            primary_nav.append({'name': 'Checkout', 'url': 'stqpictures:checkout'})
            primary_nav.append({'name': 'Logout', 'url': 'stqpictures:logout'})
        else:
            primary_nav.append({'name': 'Login', 'url': 'stqpictures:login'})
            primary_nav.append({'name': 'Guest Checkout', 'url': 'stqpictures:guest_checkout'})

        secondary_nav = []
        if page_name in secondary_nav_pages:
            secondary_nav = [
                {'name': 'Nature', 'url': 'stqpictures:nature'},
                {'name': 'Mzansi', 'url': 'stqpictures:mzansi'},
                {'name': 'Cart', 'url': 'stqpictures:cart'},
                {'name': 'Saved for Later', 'url': 'stqpictures:save_for_later'},
            ]

        show_back_forward = page_name in ['add-to-cart', 'save-for-later', 'checkout', 'blog']

        context = {
            'page_name': page_name,
            'primary_nav': primary_nav,
            'secondary_nav': secondary_nav,
            'show_back_forward': show_back_forward,
        }

        # Handle specific page rendering
        if page_name == "blog":
            context['blog_posts'] = BlogPost.objects.all().order_by('-published_date')
        elif page_name == "mzansi":
            context['range_mzansi'] = range(1, 17)
        elif page_name == "nature":
            context['range_nature'] = range(1, 9)
        elif page_name == "services":
            context['services'] = Service.objects.all()
            return render(request, "stqpictures/service_list.html", context)
        elif page_name == "products":
            context['products'] = Product.objects.all()
            return render(request, "stqpictures/product_list.html", context) 

        # Search functionality
        if 'q' in request.GET:
            query = request.GET.get('q')
            blog_results = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
            service_results = Service.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
            results = (
                [{'title': blog.title, 'url': 'stqpictures:blog_detail', 'type': 'blog'} for blog in blog_results] +
                [{'title': service.name, 'url': 'stqpictures:service_detail', 'type': 'service'} for service in service_results]
            )
            context['results'] = results
            context['query'] = query

        return render(request, f"stqpictures/{page_name}.html", context)


# Function to get the exchange rate (converted to a class method for consistency)
class CurrencyConverter:
    @staticmethod
    def get_exchange_rate(from_currency="ZAR", to_currency="ZAR"):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()
            return data['rates'].get(to_currency, 1)
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return 1  # Default to 1 if API fails


# Product Detail View with Currency Conversion
class ProductDetailView(DetailView):
    model = Product
    template_name = 'stqpictures/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_currency = self.request.GET.get('currency', 'ZAR')
        exchange_rate = CurrencyConverter.get_exchange_rate("ZAR", selected_currency)

        product = context['product']
        product.converted_price = round(product.price * exchange_rate, 2)

        context['selected_currency'] = selected_currency
        return context
    
class ProductListView(ListView):
    model = Product
    template_name = 'stqpictures/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.all()
        sort_option = self.request.GET.get('sort', 'name-a-z')  # Default sorting

        # Apply sorting logic
        if sort_option == 'price-low-high':
            queryset = queryset.order_by('price')
        elif sort_option == 'price-high-low':
            queryset = queryset.order_by('-price')
        elif sort_option == 'name-a-z':
            queryset = queryset.order_by('name')
        elif sort_option == 'name-z-a':
            queryset = queryset.order_by('-name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_currency = self.request.GET.get('currency', 'ZAR')  # Default to ZAR
        exchange_rate = CurrencyConverter.get_exchange_rate("ZAR", selected_currency)

        for product in context['products']:
            product.converted_price = product.price * exchange_rate

        context.update({
            'selected_currency': selected_currency,
            'exchange_rate': exchange_rate,
            'sort_option': self.request.GET.get('sort', 'name-a-z')
        })
        return context


class ServiceListView(ListView):
    model = Service
    template_name = 'stqpictures/service_list.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        queryset = Service.objects.all()
        sort_option = self.request.GET.get('sort', 'name-a-z')  # Default sorting

        # Apply sorting logic
        if sort_option == 'price-low-high':
            queryset = queryset.order_by('price')
        elif sort_option == 'price-high-low':
            queryset = queryset.order_by('-price')
        elif sort_option == 'name-a-z':
            queryset = queryset.order_by('name')
        elif sort_option == 'name-z-a':
            queryset = queryset.order_by('-name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_currency = self.request.GET.get('currency', 'ZAR')  # Default to ZAR
        exchange_rate = CurrencyConverter.get_exchange_rate("ZAR", selected_currency)

        for service in context['services']:
            service.converted_price = service.price * exchange_rate

        context.update({
            'selected_currency': selected_currency,
            'exchange_rate': exchange_rate,
            'sort_option': self.request.GET.get('sort', 'name-a-z')
        })
        return context

# Service Detail View with Currency Conversion
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'stqpictures/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_currency = self.request.GET.get('currency', 'ZAR')
        exchange_rate = CurrencyConverter.get_exchange_rate("ZAR", selected_currency)

        service = context['service']
        service.converted_price = round(service.price * exchange_rate, 2)

        context['selected_currency'] = selected_currency
        return context

# Competition Entry CreateView
class CompetitionEntryCreateView(CreateView):
    model = CompetitionEntry
    fields = ["name", "email", "phone", "category", "upload_link"]
    template_name = "stqpictures/competitions/stq_svcfranchise.html"
    success_url = reverse_lazy("competition_entry")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_20_contestants"] = CompetitionEntry.objects.filter(active=True).order_by("-submission_date")[:20]
        context["winner"] = context["top_20_contestants"].first() if context["top_20_contestants"] else None
        return context

# Competition ListView
class CompetitionListView(ListView):
    model = CompetitionEntry
    template_name = "stqpictures/competitions/stq_svcfranchise.html"
    context_object_name = "top_20_contestants"
    queryset = CompetitionEntry.objects.filter(active=True).order_by("-submission_date")[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["winner"] = self.get_queryset().first() if self.get_queryset() else None
        return context

# Music Video Production Views 
class MusicVideoProductionView(TemplateView):
    template_name = "stqpictures/departments/music_video.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Read the JSON file
        with open('static/stqpictures/data/music_video_packages.json', 'r') as file:
            data = json.load(file)

        # Pass the data as context
        context['service'] = data['service']
        context['packages'] = data['packages']
        context['additional_services'] = data['additional_services']
        context['booking_details'] = data['booking_details']

        return context


# ✅ Video Listing View
class VideoListView(View):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()  # Fetch all uploaded videos

        # Static videos for UI/Promotions
        static_videos = [
            {'title': 'Promo Video', 'url': '/static/videos/promo.mp4'},
            {'title': 'Tutorial Video', 'url': '/static/videos/tutorial.mp4'}
        ]
        return render(request, 'video_list.html', {'videos': videos, 'static_videos': static_videos})

# ✅ Serve Individual Video
class VideoDetailView(View):
    def get(self, request, video_id, *args, **kwargs):
        video = get_object_or_404(Video, id=video_id)

        # If it's an uploaded video, serve the file directly
        if video.video_file:
            response = HttpResponse(video.video_file, content_type='video/mp4')
            response['Content-Disposition'] = f'inline; filename="{video.title}.mp4"'
            return response

        return render(request, 'video_detail.html', {'video': video})

# ✅ Video Upload View (Authenticated Users Only)
class VideoUploadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = VideoForm()
        return render(request, 'upload_video.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user  # Assign uploader
            video.save()
            return redirect('video-list')
        return render(request, 'upload_video.html', {'form': form})


# STQ_SVCFranchise Views
class FranchiseView(View):
    def get(self, request, *args, **kwargs):
        # Now referencing the correct template path
        return render(request, 'stqpictures/competitions/stq_svcfranchise.html')
    
# Search Views 
class SearchView(ListView):
    template_name = 'stqpictures/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if query:
            product_results = Product.objects.filter(name__icontains=query)
            service_results = Service.objects.filter(name__icontains=query)
            blog_results = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        else:
            product_results = Service.objects.none()
            service_results = Service.objects.none()
            blog_results = BlogPost.objects.none()

        return list(product_results) + list(service_results) + list(blog_results)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # ✅ Pass search query for the template
        return context


# Views for 'privacy' and 'terms'
class PrivacyView(TemplateView):
    template_name = 'stqpictures/privacy.html'  # Path to your privacy policy template

class TermsView(TemplateView):
    template_name = 'stqpictures/terms.html'    # Path to your terms of service template
    