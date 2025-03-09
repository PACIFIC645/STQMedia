from django.urls import path
from .views import theme_home

urlpatterns = [
    path('', theme_home, name='theme_home'),
]
