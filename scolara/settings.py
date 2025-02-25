"""
Django settings for scolara project.

Generated by 'django-admin startproject' using Django 5.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = 'django-insecure-e-zzhv3vp31kv4ekm^m)%n_piwqvx!9#l7tq@w@lhtwbntqxub'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True  # Permettre l'envoi de cookies

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True

# Ou pour spécifier certaines origines :
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Remplacez par l'URL de votre frontend
    "http://127.0.0.1:3000", 
    "https://scolara-front.onrender.com",
    "https://scolara-backend.onrender.com", # Remplacez par l'URL de votre frontend
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'scolarapp',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_extensions',
    'storages',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware', 
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}

ROOT_URLCONF = 'scolara.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'scolara.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  
#         'NAME': 'scolara_database',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',  
#         'PORT': '3306',  
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scolaradatabase',
        'USER': 'admin',
        'PASSWORD': 'Daasmaaoune123_',
        'HOST': 'scolara-database.cvyg2wuy2xws.eu-north-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'ssl': {'check_same_thread': False},  # Ajoutez cette option pour désactiver SSL si nécessaire
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# AUTH_USER_MODEL = 'scolarapp.User'

# MEDIA_URL = 'https://scolara-bucket.s3.eu-north-1.amazonaws.com/'


AUTH_USER_MODEL = 'scolarapp.User'
SENDINBLUE_API_KEY = os.environ.get('SENDINBLUE_API_KEY')
SMS_API_KEY = os.environ.get('SMS_API_KEY')
FRONTEND_URL = "http://localhost:3000"

ORS_API_KEY= os.getenv("https://maps.openrouteservice.org/#/directions/Oued%20Zrida,Maroc/Jorf%20Ennaga,Maroc/Bou%20Zoukenni,Maroc/data/55,130,32,198,15,97,4,224,38,9,96,59,2,24,5,192,166,6,113,0,184,64,90,0,216,3,164,32,118,1,57,8,3,140,129,88,0,98,121,134,4,96,6,128,102,79,136,9,151,138,0,88,43,85,104,44,112,186,172,3,115,230,172,65,184,138,21,122,181,168,217,175,46,189,138,12,231,80,171,78,139,90,180,43,204,161,89,101,136,85,102,192,239,13,44,58,117,103,206,133,75,203,106,114,27,218,144,132,29,132,2,0,1,213,30,2,17,27,7,20,0,11,202,0,22,215,26,132,44,58,2,0,12,222,0,6,221,23,4,22,26,30,0,13,201,0,28,223,0,2,194,180,184,36,3,61,11,61,26,29,17,12,0,175,13,178,9,41,61,182,29,22,1,188,50,58,54,52,3,59,47,61,0,31,76,57,26,25,9,34,100,13,179,21,4,172,12,102,55,20,26,185,30,41,45,23,11,57,23,51,29,0,23,198,230,232,0,0")

AWS_STORAGE_BUCKET_NAME = 'scolara-backend-bucket'  # Remplacez par le vrai nom
AWS_S3_REGION_NAME = 'eu-north-1'  # Remplacez par la bonne région
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

FRONTEND_URL = "https://scolara-front.onrender.com"

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_QUERYSTRING_AUTH = False  # Désactive les URL signées (fichiers publics)
AWS_S3_FILE_OVERWRITE = False  # Évite l'écrasement des fichiers
AWS_DEFAULT_ACL = None  # Requis pour certains paramètres par défaut
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },

    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    }
}

TWILIO_ACCOUNT_SID =  os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN =  os.environ.get('TWILIO_AUTH_TOKEN')
MESSAGING_SERVICE_SID = os.environ.get('MESSAGING_SERVICE_SID')


