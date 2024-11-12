"""
Django settings for ashapro1 project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from pathlib import Path
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api


load_dotenv()
GROQ_API_KEY=os.getenv('GROQ_API_KEY')



CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default_secret_key')

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','localhost','asha2.onrender.com']

SITE_ID = 2
# Application definition


INSTALLED_APPS = [
   
    'cloudinary',
    'cloudinary_storage',
      
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ashaapp1',
    'predictor',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 
   
    
  
]




SOCIALACCOUNT_PROVIDERS = {
    'google': {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online"
        }
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  #newly added
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
  
    
]


ROOT_URLCONF = 'ashapro1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'ashapro1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Static Files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # This points to your static directory
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



  # If you have local static files


 # This ensures static files are collected here

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'





# Cloudinary will serve static files
#STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'


# Media Files (user uploads)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = 'https://res.cloudinary.com/djum0pvam/media/'
        #subdirectories should be added here (media/images)


#DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


SOCIALACCOUNT_ADAPTER = 'ashaapp1.adapters.MySocialAccountAdapter'



LOGIN_URL = '/login/'  # Or the URL name you have for your login view

LOGIN_REDIRECT_URL = '/wellness/'
LOGOUT_REDIRECT_URL = '/'

# New settings to skip intermediate pages
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True


# yourproject/settings.py

# ... your other settings ...

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
 # Your email password or app password

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')




# MSG91_AUTH_KEY = '431161ATc7Mf1qc6666f3ef0cP1'
# MSG91_TEMPLATE_ID = ''




# settings.py

# MSG91_API_KEY = '431161ATc7Mf1qc6666f3ef0cP1'
# MSG91_SENDER_ID = 'msgind'
# MSG91_ROUTE = '4'  # Default route for transactional messages
# MSG91_COUNTRY = '91'  # Country code for India
# MSG91_TEMPLATE_ID = '670026bbd6fc054000692e52' 


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
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'cloudinary': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
