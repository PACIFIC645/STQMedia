# Core Django imports
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

# Custom Views
from .views import (
    IndexView, AboutView, CentralView, GalleryView, NatureView, MzansiView, BlogDetailView, 
    BlogListView, ContactView, GuestCheckoutView, CheckoutView, SaveForLaterView, SearchView, 
    VideoListView, VideoDetailView, VideoUploadView, AddToCartView, CartView, CustomLoginView, 
    LogoutView, ServiceListView, ServiceDetailView, ProductListView, ProductDetailView, 
    CompetitionEntryCreateView, CompetitionListView, MusicVideoProductionView, FranchiseView, 
    PrivacyView, TermsView, RegisterView, ProfileUpdateView, ProfilePictureUpdateView, 
    UserProfileView, GalleryPreviewView
)

# Define the namespace for app URLs
app_name = 'stqpictures'

urlpatterns = [
    # Home page
    path('', IndexView.as_view(), name='home'),

    # About page
    path('about/', AboutView.as_view(), name='about'),

    # User Registration
    path('accounts/register/', RegisterView.as_view(), name='register'),

    # Login/Logout
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Profile (for logged-in users)
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Profile Update
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/update/picture/', ProfilePictureUpdateView.as_view(), name='profile-picture-update'),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Gallery pages
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('gallery-preview/', GalleryPreviewView.as_view(), name='gallery_preview'),

    # Mzansi and Nature pages
    path('mzansi/', MzansiView.as_view(), name='mzansi'),
    path('nature/', NatureView.as_view(), name='nature'),

    # Blog page
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),

    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_redirect/', BlogListView.as_view(), name='blog'),  # Only if you want this as a redirect 

    # Video page
    path('videos/', VideoListView.as_view(), name='video-list'),  # ✅ Show all videos
    path('video/<int:video_id>/', VideoDetailView.as_view(), name='video-detail'),  # ✅ Serve individual video
    
    path('upload/', VideoUploadView.as_view(), name='upload-video'),

    # Contact page
    path('contact/', ContactView.as_view(), name='contact'),

    # STQ_SVCFranchise competitions page
    path('franchise/', FranchiseView.as_view(), name='stq_svcfranchise'),

    # Checkout and related pages
    path('guest-checkout/', GuestCheckoutView.as_view(), name='guest_checkout'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    
    # Save for Later
    path('save-for-later/', SaveForLaterView.as_view(), name='save_for_later'),

    # Add-to-cart functionality
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'), 

    # Search for items
    path('search/', SearchView.as_view(), name='search'),
    
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),

    # Add the URL for viewing the cart
    path('cart/', CartView.as_view(), name='cart'),  # Replace CartView with your actual cart view.

    # Dynamic CentralView Route
    path('<str:page_name>/', CentralView.as_view(), name='central'),  # Handles dynamic pages

    # Static Navigation Route
    path('central/', CentralView.as_view(), name='central'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),

    path("competition/", CompetitionEntryCreateView.as_view(), name="competition_entry"),
    path("competition/list/", CompetitionListView.as_view(), name="competition_list"),

    path("services/music-video/", MusicVideoProductionView.as_view(), name="music_video"),

    path('privacy/', PrivacyView.as_view(), name='privacy'),  # Ensure this is defined
    path('terms/', TermsView.as_view(), name='terms'),  # Assuming you have a terms view

    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('stqpictures/images/favicon.ico'))),
]
