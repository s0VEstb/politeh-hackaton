import os
from pathlib import Path
from decouple import config
from datetime import timedelta


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROD = config('PROD', default=False, cast=bool)


if PROD:
    from .prod import *
    from .cors import *

else:
    from .dev import *
    from .cors import *


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.gis',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'rest_framework_gis',
    'leaflet',  
    'corsheaders',
    'rest_framework.authtoken',           
    'djoser',
    'drf_spectacular',
    'rest_framework_simplejwt.token_blacklist',

    'apps.map',
    'apps.users',
]

AUTH_USER_MODEL = 'users.User'

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (42.8806, 74.6174),
    'DEFAULT_ZOOM': 12,
    'MIN_ZOOM': 5,
    'MAX_ZOOM': 18,
}


MIDDLEWARE = [
    # 1) CorsMiddleware идёт первым
    'corsheaders.middleware.CorsMiddleware',

    # 2) Затем стандартные Django-мидлвары безопасности и сессий
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # 3) После них — CommonMiddleware, чтобы он прочитал CORS-заголовки
    'django.middleware.common.CommonMiddleware',

    # 4) Дальше — остальные
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # этот класс будет проверять заголовок Bearer <token>
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # (опционально) если вам нужны сессии, можно добавить
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    # (опционально) разрешить доступ только аутентифицированным по умолчанию
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API Документация',
    'DESCRIPTION': 'Документация к API регистрации, активации и JWT-аутентификации',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
}



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,  # нужно для автоматической ротации
    'BLACKLIST_AFTER_ROTATION': True,  # чтобы добавлять старые токены в blacklist
    'AUTH_HEADER_TYPES': ('Bearer',),
}



DJOSER = {
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'TOKEN_MODEL': None,  # выключаем стандартный DRF Token
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'api/auth/activate/{uid}/{token}/',  
    'SERIALIZERS': {
        'user_create': 'apps.users.serializers.UserCreateSerializer',
        'user': 'apps.users.serializers.UserSerializer',
        'activation': 'djoser.serializers.ActivationSerializer',
        'current_user': 'apps.users.serializers.UserSerializer',

    },
    'VIEWS': {
        # Заменяем стандартную вьюху «activation» на нашу
        'activation': 'apps.users.views.ActivationGetView',
    },
}


ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'



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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'back_static/'
STATIC_ROOT = os.path.join(BASE_DIR,'back_static')

MEDIA_URL = 'back_media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'back_media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'attokurov090506@gmail.com'
EMAIL_HOST_PASSWORD = 'vnhp plob bqud flkh'
DEFAULT_FROM_EMAIL = 'Hackaton <no-reply@example.com>'

