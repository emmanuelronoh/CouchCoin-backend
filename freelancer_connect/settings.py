"""
Django settings for freelancer_connect project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-p7mc5)0i1t1!sv68eyqfr+^%8@-_p=u6n7&6)92@4*%4f&pd6l')

AUTH_USER_MODEL = 'users.User'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

def get_user_model():
    from users.models import User  # ✅ Import inside function to avoid early execution
    return User

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # React Native frontend
]

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]


INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',


    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',  # Required for token authentication
    'rest_framework_simplejwt',
    'corsheaders',

    # Authentication apps
    'django.contrib.sites',  # Required for django-allauth
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'django_filters',
    

    # Custom apps
    'users',
    'jobs',
]

# Required for django-allauth
SITE_ID = 1  # Ensure this matches the correct site in your database

PASSWORD_RESET_TIMEOUT = 3600 * 24  # 24 hours


# Function to get the site dynamically after Django loads
def get_site_name():
    from django.contrib.sites.models import Site  # ✅ Correct placement
    return Site.objects.get(id=SITE_ID).domain

try:
    DOMAIN = get_site_name()  # Get domain dynamically
except Exception:
    DOMAIN = "127.0.0.1:8000"  # Fallback if DB isn't set up yet

# django-allauth settings
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Require email verification
ACCOUNT_LOGIN_METHODS = {"email"}  # Users log in with email
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True  # Email is required for registration
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Freelancer Connect "  # Email subject prefix
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_UNIQUE_EMAIL = True

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "eronoh036@gmail.com"  # Replace with your email
EMAIL_HOST_PASSWORD = "rsnw faki kyat yhzs"  # Use an App Password for Gmail
EMAIL_USE_SSL = False  # Ensure it's False since you are using TLS
EMAIL_TIMEOUT = 10  # Optional timeout for connections
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Ensure the sender is correctly set
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"



# dj-rest-auth settings
REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetSerializer',
}



# Disable dj-rest-auth's email verification view to prevent conflicts
REST_AUTH_REGISTER_SERIALIZERS = {
    'VERIFY_EMAIL': None , # Disables dj-rest-auth's email confirmation
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Added for CORS support
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    
]

ROOT_URLCONF = 'freelancer_connect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Make sure this points to your templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by Allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'freelancer_connect.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'freelancer_connect',
#         'USER': 'Emmanuel_freelance',
#         'PASSWORD': '*******',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Allowed Hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

