import os
from pathlib import Path
from decouple import config
import dj_database_url

# Base directory
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# 🔹 Load environment variables
SECRET_KEY = config('SECRET_KEY', default='django-insecure-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',  # API support
    'corsheaders',  # CORS handling
    'axes',  # Brute force attack protection

    # Custom apps
    'stqpictures',  # Core app
]

# Axes Configuration
AXES_FAILURE_LIMIT = 5  # Number of allowed failed attempts
AXES_LOCK_OUT_AT_FAILURE = True  # Lock out after exceeding the limit
AXES_COOLOFF_TIME = 1  # Lockout duration in hours
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']  # Lockout based on username and IP address
AXES_ENABLE_ADMIN = True  # Enable Axes within the Django admin

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Axes for brute force protection
    'django.contrib.auth.backends.ModelBackend',  # Default authentication backend
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Enable CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Axes Middleware
    'axes.middleware.AxesMiddleware',
]

# CORS settings
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000').split(',')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Root URL configuration
ROOT_URLCONF = 'stqmedia.urls'

# Project templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "Templates",                      # Where base.html lives
            BASE_DIR / "stqpictures" / "Templates",        # Where the app templates and includes are located
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'stqmedia.wsgi.application'

# Database configuration
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL', default='postgres://stqmedia_user:password@127.0.0.1:5432/stqmedia_db')
#     )
# }


# Database configuration
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Staticfiles settings 
STATIC_URL = '/static/'

# Static files locations
STATICFILES_DIRS = [
    '/mnt/c/Users/user/Pictures/STQMEDIA/theme/static_src',  # Bundled JS & CSS
    '/mnt/c/Users/user/Pictures/STQMEDIA/stqpictures/static',  # Image assets
]

# Collected static files for production
STATIC_ROOT = '/mnt/c/Users/user/Pictures/STQMEDIA/staticfiles_collected'

# Media files (uploaded by users/admin)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/mnt/c/Users/user/Pictures/STQMEDIA/media'  # Absolute path to the media folder

# STORAGES = {
#     'staticfiles': {
#         'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
#     },
# }
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

# Django Rest Framework (DRF) settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Adjust as per your security needs
    ],
}

# Redirect users to the homepage or another custom page after login/logout
LOGIN_REDIRECT_URL = 'stqpictures:home'
LOGOUT_REDIRECT_URL = 'stqpictures:home'

# Security settings
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
else:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

# CSRF settings
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'

# Logging (for production)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Correct file path resolution for JSON data
MUSIC_VIDEO_PACKAGES_PATH = BASE_DIR / 'stqpictures' / 'data' / 'music_video_packages.json'
# MUSIC_VIDEO_PATH = BASE_DIR / 'stqpictures' / 'data' / 'music_videos.json'
# PRODUCTS_PATH = BASE_DIR / 'stqpictures' / 'data' / 'products.json'
# SERVICES_PATH = BASE_DIR / 'stqpictures' / 'data' / 'services.json'

# VIDEO_PACKAGES_PATH = BASE_DIR / 'stqpictures' / 'data' / 'video_packages.json'
# VIDEO_PATH = BASE_DIR / 'stqpictures' / 'data' / 'videos.json'

# VIDEO_UPLOAD_PATH = BASE_DIR / 'stqpictures' / 'data' / 'video_upload.json'

