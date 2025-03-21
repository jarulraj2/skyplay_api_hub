"""
Django settings for skyplay_api_hub project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Allowed Hosts
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'setting',
    'subscribe',
    'razorpay',
    'django_extensions',
    'users',
    'wallet',
    'skyplay_api',
    'rest_framework',
    'drf_yasg',
    'testapp', 
    'watcho',
    'import_export',
    'channels',
    'django.contrib.sites',  # For allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'ott_subscription',  # Your app
    'corsheaders',
   
]
SITE_ID = 1

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Default
)
# Twilio settings (for phone number OTP)
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'developer@skylink.net.in'
EMAIL_HOST_PASSWORD = 'dkoqlcsxagoywdeh'
# Optional settings (you can leave them out if not needed)
DEFAULT_FROM_EMAIL = 'developer@skylink.net.in'  # Default from email (optional)
EMAIL_SUBJECT_PREFIX = '[SKYLINK] '  # Optional prefix for email subject lines




MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Add this line
]

# Allow all origins for development purposes
CORS_ALLOW_ALL_ORIGINS = True

CSRF_COOKIE_HTTPONLY = True  # This makes the CSRF cookie inaccessible to JavaScript.
CSRF_COOKIE_SECURE = False  # Set to True if you're using HTTPS.

ROOT_URLCONF = 'skyplay_api_hub.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'skyplay_api_hub.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DJANGO_DATABASE_NAME', 'skyplay_api_hub3'),
        'USER': os.getenv('DJANGO_DATABASE_USER', 'root'),
        'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD', ''),
        'HOST': os.getenv('DJANGO_DATABASE_HOST', '127.0.0.1'),
        'PORT': os.getenv('DJANGO_DATABASE_PORT', '3306'),
    }
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # You can change this if needed
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Razorpay API Keys
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'your-razorpay-key-id')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'your-razorpay-key-secret')

# test

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "django_errors.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}


BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')

ENCRYPTION_PASS_PHRASE = "1234"

## Ott Play
OTTPLAY_API_URL = 'https://stg-partners.ottplay.com/api/v4.0/subscriber/action'
OTTPLAY_AUTH_TOKEN = 'fRGcemrfodXg5OBXh6JDJ79MNab7QSbOxlnAlmL8VvRdCNSVBdfiHmSzwvcQ24pDOPtBD2rPu8LrU0S1gOlGZ2iegAPpEKXuvIb9b3ctf3dAQStqGuNRfZYZHEwpzontQQhrmd0EixJ1378ss7sBRonQfceHO6Jyj6La8EODIymMyqhNWURo9zlUZIDjgn19rJCfNVn42nL7OA4zSqTgsA1uyy8nVx7C89l8imSpYvs8E70uqeUzAfo3w9EUpP1',
OTTPLAY_LOGIN_ID = 'skylink_testISP'
OTTPLAY_OPER_CODE = '10276'